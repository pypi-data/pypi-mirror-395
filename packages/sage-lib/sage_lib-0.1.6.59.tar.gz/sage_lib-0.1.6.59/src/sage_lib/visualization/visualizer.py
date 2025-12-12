#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
impostor_viewer_gpu_browser.py — GPU-side supercell replication + dataset browser

Highlights
----------
- Sphere impostors with one instanced draw for all atoms in all replicas (TBOs).
- Lattice box drawn with instancing for all replicas.
- Dataset browser: next/prev/jump-to index; loads structures on the fly.
- Optional: keep camera view across structures, or auto-reset to bounds.
- Color modes: element palette vs uniform; runtime setters.

Hotkeys
-------
Left/Right         : previous / next structure
PageUp/PageDown    : -10 / +10
Home/End           : first / last
G                  : go-to mode (type digits, Enter to jump, Backspace to edit, Esc to cancel)
T                  : toggle keep-view (keep orientation+distance, only recenter) vs auto-reset
C                  : toggle color mode (palette ↔ uniform)
[ / ]              : replicas 3D radius -- / ++
, / .              : replicas XY-only -- / ++   (Z unchanged)  [useful for superficies]
B                  : toggle filled faces of central box
Shift + B          : toggle drawing boxes for all replicas
P                  : screenshot
F                  : toggle FPS in title
V                  : toggle vsync
R                  : reset camera (on current structure)
Esc                : quit
"""

from __future__ import annotations
import math, time, os
from dataclasses import dataclass, field
from typing import Optional, Sequence, Tuple, Dict, List, Protocol
import numpy as np
import glfw
from OpenGL.GL import *
from .PartitionProvider import PartitionProvider

# ---------- Element palette ----------
CPK_COLORS = {
    'H':(1.0,1.0,1.0),'C':(0.20,0.20,0.20),'N':(0.19,0.31,0.97),'O':(1.00,0.05,0.05),
    'F':(0.56,0.88,0.31),'Cl':(0.12,0.94,0.12),'Br':(0.65,0.16,0.16),'I':(0.58,0.00,0.58),
    'S':(1.00,0.78,0.20),'P':(1.00,0.50,0.00),'K':(0.56,0.25,0.83),'Na':(0.67,0.36,0.95),
    'Ni':(0.31,0.82,0.31),'Fe':(0.88,0.40,0.20),'V':(0.65,0.65,0.67), 'Cu':(0.72, 0.45, 0.20), 
}
VDW_RADII = {'H':.50,'C':1.70,'N':1.55,'O':0.92,'F':1.47,'Cl':1.75,'Br':1.85,'I':1.98,'S':1.80,'P':1.80,'K':2.75,'Na':2.27,'Ni':1.63,'Fe':1.63,'V':1.53}
DEFAULT_COLOR=(0.78,0.78,0.78); DEFAULT_RADIUS=1.2
WORLD_UP = np.array([0,0,1], dtype=np.float32)

# ---------- Math ----------
def perspective(fovy_deg: float, aspect: float, znear: float, zfar: float) -> np.ndarray:
    f = 1.0 / math.tan(math.radians(fovy_deg) / 2.0)
    M = np.zeros((4, 4), dtype=np.float32)
    M[0, 0] = f / aspect; M[1, 1] = f
    M[2, 2] = (zfar + znear) / (znear - zfar)
    M[2, 3] = (2 * zfar * znear) / (znear - zfar)
    M[3, 2] = -1.0
    return M

def look_at(eye: np.ndarray, center: np.ndarray, up: np.ndarray) -> np.ndarray:
    f = center - eye; f = f / (np.linalg.norm(f) + 1e-12)
    u = up / (np.linalg.norm(up) + 1e-12)
    s = np.cross(f, u); s = s / (np.linalg.norm(s) + 1e-12)
    u = np.cross(s, f)
    M = np.eye(4, dtype=np.float32); M[0,:3]=s; M[1,:3]=u; M[2,:3]=-f
    T = np.eye(4, dtype=np.float32); T[:3,3] = -eye
    return M @ T

def compute_bounds(points: np.ndarray):
    return points.min(axis=0), points.max(axis=0)

def cell_corners(lattice: np.ndarray) -> np.ndarray:
    a,b,c = lattice[0], lattice[1], lattice[2]; O = np.zeros(3, dtype=np.float32)
    return np.array([O, a, b, c, a+b, a+c, b+c, a+b+c], dtype=np.float32)

CELL_EDGES = np.array([[0,1],[0,2],[0,3],[1,4],[1,5],[2,4],[2,6],[3,5],[3,6],[4,7],[5,7],[6,7]], dtype=np.int32)

def normalize(v: np.ndarray) -> np.ndarray:
    n = float(np.linalg.norm(v)); 
    return v / (n if n>1e-12 else 1.0)

def rodrigues(v: np.ndarray, axis: np.ndarray, angle: float) -> np.ndarray:
    k = normalize(axis); c = math.cos(angle); s = math.sin(angle)
    return v*c + np.cross(k, v)*s + k*np.dot(k, v)*(1.0 - c)

# ---------- GL helpers ----------
def safe_gl_line_width(target: float = 1.0):
    try:
        rng = glGetFloatv(GL_ALIASED_LINE_WIDTH_RANGE)
        lo = float(rng[0]); hi = float(rng[1]) if len(rng)>=2 else float(rng[0])
    except Exception:
        lo, hi = 1.0, 1.0
    glLineWidth(max(lo, min(hi, float(target))))

def compile_shader(stage: int, src: str) -> int:
    sid = glCreateShader(stage); glShaderSource(sid, src); glCompileShader(sid)
    if not glGetShaderiv(sid, GL_COMPILE_STATUS):
        raise RuntimeError(glGetShaderInfoLog(sid).decode()); 
    return sid

def link_program(vs: str, fs: str) -> int:
    v = compile_shader(GL_VERTEX_SHADER, vs); f = compile_shader(GL_FRAGMENT_SHADER, fs)
    pid = glCreateProgram(); glAttachShader(pid, v); glAttachShader(pid, f); glLinkProgram(pid)
    if not glGetProgramiv(pid, GL_LINK_STATUS):
        raise RuntimeError(glGetProgramInfoLog(pid).decode())
    glDeleteShader(v); glDeleteShader(f); return pid

# ---------- Shaders (TBO-based) ----------
SPHERE_VS = r"""
#version 330 core
layout(location=0) in vec2 aQuad;            // (-1,-1),(1,-1),(-1,1),(1,1) for TRIANGLE_STRIP

uniform mat4 uView;
uniform mat4 uProj;
uniform samplerBuffer uAtomPosRad;           // RGBA32F: xyz=pos, w=radius (Å)
uniform samplerBuffer uAtomColor;            // RGBA32F: xyz=color [0,1], w=unused
uniform samplerBuffer uReplicaOffsets;       // RGBA32F: xyz=offset (Å)
uniform int uAtomCount;

out VS_OUT { vec3 centerVS; float radiusVS; vec3 color; vec3 posVS; } v;

void main(){
    int inst = gl_InstanceID;
    int atomIdx = inst % uAtomCount;
    int repIdx  = inst / uAtomCount;

    vec4 pr   = texelFetch(uAtomPosRad, atomIdx);
    vec3 col  = texelFetch(uAtomColor,  atomIdx).rgb;
    vec3 offs = texelFetch(uReplicaOffsets, repIdx).xyz;

    vec3 worldCenter = pr.xyz + offs;
    vec3 centerVS = vec3(uView * vec4(worldCenter, 1.0));
    float radiusVS = pr.w;

    vec3 rightVS = vec3(1,0,0);
    vec3 upVS    = vec3(0,1,0);
    vec3 cornerVS = centerVS + (aQuad.x * rightVS + aQuad.y * upVS) * radiusVS;

    v.centerVS = centerVS; v.radiusVS = radiusVS; v.color = col; v.posVS = cornerVS;
    gl_Position = uProj * vec4(cornerVS, 1.0);
}
"""

SPHERE_FS = r"""
#version 330 core
in VS_OUT { vec3 centerVS; float radiusVS; vec3 color; vec3 posVS; } v;
uniform mat4 uProj;
uniform vec3 uLightDirVS;
uniform int  uColorMode;     // 0=palette/TBO, 1=uniform
uniform vec3 uUniformColor;  // used if uColorMode==1
out vec4 fragColor;
float depthFromView(vec3 pVS){
    vec4 clip = uProj * vec4(pVS,1.0);
    float ndc = clip.z/clip.w;
    return 0.5*ndc + 0.5;
}
void main(){
    vec3 ro = vec3(0);
    vec3 rd = normalize(v.posVS - ro);
    vec3 oc = ro - v.centerVS;
    float b = dot(oc, rd);
    float c = dot(oc, oc) - v.radiusVS*v.radiusVS;
    float h = b*b - c;
    if(h<0.0) discard;
    float t = -b - sqrt(h);
    vec3 hitVS = ro + t*rd;
    vec3 N = normalize(hitVS - v.centerVS);
    float ndotl = max(dot(N, normalize(uLightDirVS)), 0.0);
    float rim = pow(1.0 - max(dot(N, -rd), 0.0), 3.0);
    vec3 base = (uColorMode==0) ? v.color : uUniformColor;
    vec3 rgb = base * (0.18 + 0.82*ndotl) + 0.12*rim;
    gl_FragDepth = depthFromView(hitVS);
    fragColor = vec4(rgb, 1.0);
}
"""

LINE_VS = r"""
#version 330 core
layout(location=0) in vec3 aPos;
uniform mat4 uView; uniform mat4 uProj;
uniform samplerBuffer uReplicaOffsets;  // RGBA32F: xyz=offset
void main(){
    vec3 offs = texelFetch(uReplicaOffsets, gl_InstanceID).xyz;
    gl_Position = uProj * uView * vec4(aPos + offs, 1.0);
}
"""
LINE_FS = r"""
#version 330 core
out vec4 fragColor;
uniform vec4 uRGBA;
void main(){ fragColor = uRGBA; }
"""

PICK_VS = r"""
#version 330 core
layout(location=0) in vec2 aQuad;
uniform mat4 uView;
uniform mat4 uProj;
uniform samplerBuffer uAtomPosRad;
uniform samplerBuffer uReplicaOffsets;
uniform int uAtomCount;

out vec3 vColorID;

void main() {
    int inst = gl_InstanceID;
    int atomIdx = inst % uAtomCount;
    int repIdx  = inst / uAtomCount;

    vec4 pr   = texelFetch(uAtomPosRad, atomIdx);
    vec3 offs = texelFetch(uReplicaOffsets, repIdx).xyz;

    vec3 worldCenter = pr.xyz + offs;
    vec3 centerVS = vec3(uView * vec4(worldCenter, 1.0));
    float radiusVS = pr.w;
    vec3 cornerVS = centerVS + vec3(aQuad, 0.0) * radiusVS;

    vColorID = vec3(
        (float((atomIdx >>  0) & 255)) / 255.0,
        (float((atomIdx >>  8) & 255)) / 255.0,
        (float((atomIdx >> 16) & 255)) / 255.0
    );
    gl_Position = uProj * vec4(cornerVS, 1.0);
}
"""

PICK_FS = r"""
#version 330 core
in vec3 vColorID;
out vec4 fragColor;
void main() { fragColor = vec4(vColorID, 1.0); }
"""

# ---------- Camera ----------
@dataclass
class OrbitCamera:
    center: np.ndarray
    offset: np.ndarray
    fov: float = 45.0
    yaw_v: float = 0.0
    pitch_v: float = 0.0
    pan_v: np.ndarray = field(default_factory=lambda: np.zeros(2, dtype=np.float32))
    zoom_v: float = 0.0
    def eye(self) -> np.ndarray: return self.center + self.offset
    def forward(self) -> np.ndarray: return normalize(-self.offset)
    def right(self) -> np.ndarray: return normalize(np.cross(self.forward(), WORLD_UP))
    def rotate_yaw(self, ang: float): self.offset = rodrigues(self.offset, WORLD_UP, ang)
    def rotate_pitch(self, ang: float):
        f = self.forward(); up_dot = float(np.dot(f, WORLD_UP))
        max_elev = math.radians(88.0); cur = math.asin(np.clip(up_dot, -1.0, 1.0))
        ang = float(np.clip(ang, -max_elev - cur, max_elev - cur))
        self.offset = rodrigues(self.offset, self.right(), ang)

# ---------- Provider Protocol ----------
class StructureProvider(Protocol):
    def __len__(self) -> int: ...
    def get(self, idx: int) -> Tuple[np.ndarray, np.ndarray, float, Optional[Sequence[str]], Optional[np.ndarray], Optional[np.ndarray]]:
        """
        Return (positions(N,3), lattice(3,3), energy, elements|None, colors|None, radii|None)
        """

    def get_all_E(self, ):
        """
        """      

    def get_all_Ef(self, ):
        """
        """     

    def get_all_compositions(self, ):
        """
        """    

# ---------- Viewer ----------
class Viewer:
    def __init__(self, provider: StructureProvider,
                 start_index: int = 0,
                 replicas: Tuple[int,int,int] = (0,0,0),
                 draw_boxes_for_all: bool = False,
                 uniform_color: Optional[Tuple[float,float,float]] = None,
                 palette: Optional[Dict[str, Tuple[float,float,float]]] = None,
                 keep_view: bool = False,
                 win_size=(1280, 800)):
        # ENERGY plot
        self.all_energies = np.array(provider.get_all_Ef(), dtype=np.float32)
        self.energy_min = float(self.all_energies.min())
        self.energy_max = float(self.all_energies.max())
        self.plot_alpha = 0.1  # between 0 (invisible) and 1 (opaque)
        self.show_energy_plot = True

        # SORT
        self.sorted_indices = np.arange(len(self.all_energies), dtype=int)
        self.sorted_by_energy = False

        # SELETION
        self.selected_atoms = []         # store selected atom indices
        self.measure_mode = False        # toggle measurement mode

        self.provider = provider
        self.index = int(max(0, min(len(provider)-1, start_index)))
        self.palette = palette if palette is not None else CPK_COLORS
        self.keep_view = bool(keep_view)

        # Window / GL
        if not glfw.init(): raise RuntimeError("GLFW init failed")
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        glfw.window_hint(glfw.SAMPLES, 0)
        self.win = glfw.create_window(win_size[0], win_size[1], "", None, None)
        if not self.win: glfw.terminate(); raise RuntimeError("GLFW window creation failed")
        glfw.make_context_current(self.win)
        glfw.swap_interval(1)
        self.vsync_on = True; self.show_fps = False; self.draw_faces = False
        self.draw_boxes_for_all = bool(draw_boxes_for_all)
        self.color_mode = 0  # 0 palette, 1 uniform
        self.uniform_color = np.array(uniform_color if uniform_color is not None else (0.2,0.6,1.0), dtype=np.float32)

        # Input
        self.last_x = self.last_y = None
        self.orbiting = False; self.panning = False
        self.goto_mode = False; self._goto_buf = ""
        # auto play 
        self.autoplay_on = False
        self.frames_per_second = 5.0 # Tasa predeterminada: 5 FPS
        self._time_since_last_frame = 0.0

        glfw.set_cursor_pos_callback(self.win, self._on_mouse_move)
        glfw.set_mouse_button_callback(self.win, self._on_mouse_button)
        glfw.set_scroll_callback(self.win, self._on_scroll)
        glfw.set_key_callback(self.win, self._on_key)
        glfw.set_char_callback(self.win, self._on_char)

        # GL state
        glEnable(GL_DEPTH_TEST); glDisable(GL_CULL_FACE)
        glClearColor(0.05, 0.07, 0.09, 1.0)

        # Programs
        self.sphere_prog = link_program(SPHERE_VS, SPHERE_FS)
        self.line_prog = link_program(LINE_VS, LINE_FS)
        self.pick_prog = link_program(PICK_VS, PICK_FS) # for selection shader

        # Disk/CPU data (current structure)
        positions, lattice, energy, elements, colors, radii = provider.get(self.index)
        self._ingest_structure(positions, lattice, energy, elements, colors, radii)

        # Buffers/TBOs
        self._build_sphere_quad()
        self._upload_atom_tbos()
        self._build_cell_buffers()
        self.replicas = tuple(int(max(0,r)) for r in replicas)
        self._rebuild_replica_offsets()

    def _measure_distance(self):
        i, j = self.selected_atoms
        r_i, r_j = self.pos[i], self.pos[j]
        d = np.linalg.norm(r_i - r_j)
        print(f"Distance between atoms {i} and {j}: {d:.3f} Å")

    def _sort_by_energy(self):
        order = np.argsort(self.all_energies)
        self.sorted_indices = order
        self.display_energies = self.all_energies[order]
        self.sorted_by_energy = True
        self.index = 0
        self._load_index(self.index)
        print(f"[viewer] Sorted by formation energy (ascending). Lowest Ef = {self.display_energies[0]:.6f} eV")

    def _unsort(self):
        self.sorted_indices = np.arange(len(self.all_energies), dtype=int)
        self.display_energies = self.all_energies
        self.sorted_by_energy = False
        self.index = 0
        self._load_index(self.index)
        print("[viewer] Restored original dataset order.")


    def _draw_energy_plot(self):
        if not getattr(self, "show_energy_plot", True):
            return
        energies = getattr(self, "display_energies", self.all_energies)
        if energies is None or len(energies) < 2:
            return

        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glUseProgram(self.line_prog)

        # Normalize energies to [-1, 1]
        n = len(energies)
        xs = np.linspace(-0.9, 0.9, n, dtype=np.float32)
        ys = 2.0 * (energies - self.energy_min) / (self.energy_max - self.energy_min) - 1.0
        ys *= 0.3  # shrink vertically for aesthetic reasons
        ys -= 0.55 # position near bottom of screen

        points = np.stack([xs, ys, np.zeros_like(xs)], axis=1).astype(np.float32)

        vao = glGenVertexArrays(1)
        glBindVertexArray(vao)
        vbo = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, vbo)
        glBufferData(GL_ARRAY_BUFFER, points.nbytes, points, GL_DYNAMIC_DRAW)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)

        # 2D identity transforms
        I = np.eye(4, dtype=np.float32)
        glUniformMatrix4fv(glGetUniformLocation(self.line_prog, "uView"), 1, GL_FALSE, I)
        glUniformMatrix4fv(glGetUniformLocation(self.line_prog, "uProj"), 1, GL_FALSE, I)

        # Draw the energy curve
        glUniform4f(glGetUniformLocation(self.line_prog, "uRGBA"), 1.0, 1.0, 1.0, self.plot_alpha)
        glDrawArrays(GL_LINE_STRIP, 0, n)

        # Highlight current structure
        i = self.index
        xh, yh = xs[i], ys[i]
        highlight = np.array([[xh, yh, 0.0]], dtype=np.float32)
        glBufferData(GL_ARRAY_BUFFER, highlight.nbytes, highlight, GL_DYNAMIC_DRAW)
        glUniform4f(glGetUniformLocation(self.line_prog, "uRGBA"), 1.0, 0.2, 0.2, 1.0)
        glPointSize(8.0)
        glDrawArrays(GL_POINTS, 0, 1)

        glDeleteBuffers(1, [vbo])
        glDeleteVertexArrays(1, [vao])
        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)


    def _pick_atom(self, x, y):
        w, h = glfw.get_framebuffer_size(self.win)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glUseProgram(self.pick_prog)
        glUniformMatrix4fv(glGetUniformLocation(self.pick_prog,"uView"),1,GL_FALSE,look_at(self.cam.eye(),self.cam.center,WORLD_UP).T)
        glUniformMatrix4fv(glGetUniformLocation(self.pick_prog,"uProj"),1,GL_FALSE,perspective(self.cam.fov,w/h,0.05,1000).T)
        glUniform1i(glGetUniformLocation(self.pick_prog,"uAtomCount"), self.N)
        glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_BUFFER, self.pr_tbo)
        glActiveTexture(GL_TEXTURE1); glBindTexture(GL_TEXTURE_BUFFER, self.rep_tbo)
        glUniform1i(glGetUniformLocation(self.pick_prog,"uAtomPosRad"), 0)
        glUniform1i(glGetUniformLocation(self.pick_prog,"uReplicaOffsets"), 1)
        glBindVertexArray(self.quad_vao)
        glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, self.N * len(self.replica_offsets))
        glBindVertexArray(0)

        # Read pixel
        px = glReadPixels(x, h - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
        if px is None:
            return None

        # Convert to numpy array of uint8
        px = np.frombuffer(px, dtype=np.uint8)
        if px.size < 3:
            return None

        r, g, b = int(px[0]), int(px[1]), int(px[2])
        idx = r + (g << 8) + (b << 16)
        if idx >= self.N:
            return None
        return idx

        #idx = int(r) + (int(g) << 8) + (int(b) << 16)
        #if idx < self.N:
        #    return idx
        #return None

    # ---- Ingest & camera ----
    def _ingest_structure(self, positions, lattice, energy, elements, colors, radii):
        self.pos = np.asarray(positions, dtype=np.float32).reshape(-1,3)
        self.lat = np.asarray(lattice, dtype=np.float32).reshape(3,3)
        self.energy = float(energy)
        self.N = self.pos.shape[0]

        if elements is not None and (radii is None and colors is None):
            colors_el = np.array([self.palette.get(str(e), DEFAULT_COLOR) for e in elements], dtype=np.float32)
            radii_el = np.array([VDW_RADII.get(str(e), DEFAULT_RADIUS) for e in elements], dtype=np.float32)
            radii, colors = radii_el, colors_el
        self.radii = np.asarray(radii if radii is not None else np.full((self.N,), DEFAULT_RADIUS), dtype=np.float32)
        self.colors_base = np.asarray(colors if colors is not None else np.tile(DEFAULT_COLOR, (self.N, 1)), dtype=np.float32)
        self.colors_current = self.colors_base.copy()

        # Camera center & offset
        mn, mx = compute_bounds(np.vstack([self.pos, cell_corners(self.lat)]))
        center = (mn + mx) * 0.5
        diag = float(np.linalg.norm(mx - mn))
        if not hasattr(self, 'cam') or not self.keep_view:
            offset = np.array([1.8*diag, 1.2*diag, 0.9*diag], dtype=np.float32)
            self.cam = OrbitCamera(center=center.astype(np.float32), offset=offset)
        else:
            # keep orientation+distance, recenter
            self.cam.center = center.astype(np.float32)
        glfw.set_window_title(self.win, f"[{self.index+1}/{len(self.provider)}]  Energy: {self.energy:.6f} eV   |   Atoms: {self.N}")

    # ---- Replica offsets (GPU) ----
    def _rebuild_replica_offsets(self):
        rx, ry, rz = self.replicas
        a, b, c = self.lat[0], self.lat[1], self.lat[2]
        offs = []
        for i in range(-rx, rx+1):
            for j in range(-ry, ry+1):
                for k in range(-rz, rz+1):
                    offs.append(i*a + j*b + k*c)
        offs.sort(key=lambda v: float(np.linalg.norm(v)))
        self.replica_offsets = np.array(offs, dtype=np.float32)
        self._upload_replica_tbo()

    # ---- GL buffers/tbos ----
    def _build_sphere_quad(self):
        quad = np.array([[-1,-1],[1,-1],[-1,1],[1,1]], dtype=np.float32)
        self.quad_vao = glGenVertexArrays(1); glBindVertexArray(self.quad_vao)
        self.quad_vbo = glGenBuffers(1); glBindBuffer(GL_ARRAY_BUFFER, self.quad_vbo)
        glBufferData(GL_ARRAY_BUFFER, quad.nbytes, quad, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0); glVertexAttribPointer(0, 2, GL_FLOAT, GL_FALSE, 0, None)
        glBindVertexArray(0)

    def _upload_atom_tbos(self):
        posrad = np.zeros((self.N, 4), dtype=np.float32); posrad[:, :3] = self.pos; posrad[:, 3] = self.radii
        colors = np.zeros((self.N, 4), dtype=np.float32); colors[:, :3] = self.colors_current
        # create or resize buffers
        if not hasattr(self, 'pr_bo'):
            self.pr_bo = glGenBuffers(1); self.pr_tbo = glGenTextures(1)
        glBindBuffer(GL_TEXTURE_BUFFER, self.pr_bo); glBufferData(GL_TEXTURE_BUFFER, posrad.nbytes, posrad, GL_STATIC_DRAW)
        glBindTexture(GL_TEXTURE_BUFFER, self.pr_tbo); glTexBuffer(GL_TEXTURE_BUFFER, GL_RGBA32F, self.pr_bo)

        if not hasattr(self, 'col_bo'):
            self.col_bo = glGenBuffers(1); self.col_tbo = glGenTextures(1)
        glBindBuffer(GL_TEXTURE_BUFFER, self.col_bo); glBufferData(GL_TEXTURE_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
        glBindTexture(GL_TEXTURE_BUFFER, self.col_tbo); glTexBuffer(GL_TEXTURE_BUFFER, GL_RGBA32F, self.col_bo)

        glBindBuffer(GL_TEXTURE_BUFFER, 0)

    def _update_color_tbo(self):
        # make a copy of base colors
        colors_arr = self.colors_current.copy()

        # --- highlight selected atoms in red ---
        if hasattr(self, "selected_atoms") and len(self.selected_atoms) > 0:
            for i in self.selected_atoms:
                if 0 <= i < len(colors_arr):
                    colors_arr[i] = [0.0, 1.0, 1.0]  # highlight in red

        # upload to GPU
        colors = np.zeros((self.N, 4), dtype=np.float32)
        colors[:, :3] = colors_arr
        glBindBuffer(GL_TEXTURE_BUFFER, self.col_bo)
        glBufferData(GL_TEXTURE_BUFFER, colors.nbytes, colors, GL_STATIC_DRAW)
        glBindBuffer(GL_TEXTURE_BUFFER, 0)


    def _build_cell_buffers(self):
        # delete previous if exist
        if hasattr(self, 'cell_vao'):
            try: glDeleteVertexArrays(1, [self.cell_vao]); glDeleteBuffers(1, [self.cell_vbo])
            except Exception: pass
        if hasattr(self, 'face_vao'):
            try: glDeleteVertexArrays(1, [self.face_vao]); glDeleteBuffers(1, [self.face_vbo])
            except Exception: pass

        corners = cell_corners(self.lat); edges = CELL_EDGES
        edge_count = edges.shape[0]
        line_vertices = np.empty((edge_count*2, 3), dtype=np.float32)
        line_vertices[0::2] = corners[edges[:,0]]
        line_vertices[1::2] = corners[edges[:,1]]
        self.cell_count = edge_count*2
        self.cell_vao = glGenVertexArrays(1); glBindVertexArray(self.cell_vao)
        self.cell_vbo = glGenBuffers(1); glBindBuffer(GL_ARRAY_BUFFER, self.cell_vbo)
        glBufferData(GL_ARRAY_BUFFER, line_vertices.nbytes, line_vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0); glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindVertexArray(0)

        faces = np.array([
            [0,1,4,  0,4,2],
            [3,5,7,  3,7,6],
            [0,1,5,  0,5,3],
            [2,4,7,  2,7,6],
            [0,2,6,  0,6,3],
            [1,4,7,  1,7,5],
        ], dtype=np.int32).reshape(-1,3)
        face_vertices = corners[faces].astype(np.float32)
        self.face_count = face_vertices.shape[0]
        self.face_vao = glGenVertexArrays(1); glBindVertexArray(self.face_vao)
        self.face_vbo = glGenBuffers(1); glBindBuffer(GL_ARRAY_BUFFER, self.face_vbo)
        glBufferData(GL_ARRAY_BUFFER, face_vertices.nbytes, face_vertices, GL_STATIC_DRAW)
        glEnableVertexAttribArray(0); glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
        glBindVertexArray(0)

    def _upload_replica_tbo(self):
        data = np.zeros((len(self.replica_offsets), 4), dtype=np.float32)
        data[:, :3] = self.replica_offsets
        if not hasattr(self, "rep_bo"):
            self.rep_bo = glGenBuffers(1); self.rep_tbo = glGenTextures(1)
        glBindBuffer(GL_TEXTURE_BUFFER, self.rep_bo)
        glBufferData(GL_TEXTURE_BUFFER, data.nbytes, data, GL_STATIC_DRAW)
        glBindTexture(GL_TEXTURE_BUFFER, self.rep_tbo)
        glTexBuffer(GL_TEXTURE_BUFFER, GL_RGBA32F, self.rep_bo)
        glBindBuffer(GL_TEXTURE_BUFFER, 0)

    # ----- Input -----
    def _on_char(self, win, codepoint):
        if not self.goto_mode: return
        ch = chr(codepoint)
        if ch.isdigit():
            self._goto_buf += ch
            self._flash_title(f"Goto index: {self._goto_buf}")
        # ignore others; backspace handled in key callback

    def _on_mouse_move(self, win, x, y):
        if self.last_x is None:
            self.last_x, self.last_y = x, y; return
        dx, dy = x - self.last_x, y - self.last_y
        self.last_x, self.last_y = x, y
        if self.orbiting:
            self.cam.yaw_v   += 0.003 * dx
            self.cam.pitch_v += -0.003 * dy
        elif self.panning:
            self.cam.pan_v += np.array([dx, dy], dtype=np.float32)

    def _on_mouse_button(self, win, button, action, mods):
        # --- Shift + Left Click → atom picking ---
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.RELEASE and (mods & glfw.MOD_SHIFT):
            x, y = glfw.get_cursor_pos(win)
            atom = self._pick_atom(int(x), int(y))
            if atom is not None:
                self.selected_atoms.append(atom)
                print(f"Selected atom #{atom}")
                if len(self.selected_atoms) > 2:
                    self.selected_atoms = self.selected_atoms[-2:]
                if len(self.selected_atoms) == 2:
                    self._measure_distance()
                # refresh highlight
                self._update_color_tbo()
            return

        # --- Regular Left Click → orbit ---
        if button == glfw.MOUSE_BUTTON_LEFT:
            self.orbiting = (action == glfw.PRESS)

        # --- Right Click → pan ---
        if button == glfw.MOUSE_BUTTON_RIGHT:
            self.panning = (action == glfw.PRESS)

        # --- On release, stop motion ---
        if action == glfw.RELEASE and button in (glfw.MOUSE_BUTTON_LEFT, glfw.MOUSE_BUTTON_RIGHT):
            self.orbiting = False
            self.panning = False
            self.last_x = self.last_y = None

    def _on_scroll(self, win, dx, dy): self.cam.zoom_v += -0.15 * dy

    def _on_key(self, win, key, sc, action, mods):
        if action != glfw.PRESS: return
        if self.goto_mode:
            if key == glfw.KEY_ENTER or key == glfw.KEY_KP_ENTER:
                if self._goto_buf:
                    idx = max(0, min(len(self.provider)-1, int(self._goto_buf)))
                    self._load_index(idx)
                self.goto_mode = False; self._goto_buf = ""
            elif key == glfw.KEY_BACKSPACE:
                self._goto_buf = self._goto_buf[:-1]
                self._flash_title(f"Goto index: {self._goto_buf}")
            elif key == glfw.KEY_ESCAPE:
                self.goto_mode = False; self._goto_buf = ""; self._flash_title("")
            return

        if key == glfw.KEY_ESCAPE: glfw.set_window_should_close(self.win, True)
        elif key == glfw.KEY_R: self._reset_camera()
        elif key == glfw.KEY_P: self._save_screenshot()
        elif key == glfw.KEY_F: self.show_fps = not self.show_fps
        elif key == glfw.KEY_V: self.vsync_on = not self.vsync_on; glfw.swap_interval(1 if self.vsync_on else 0)
        elif key == glfw.KEY_B:
            if (glfw.get_key(self.win, glfw.KEY_LEFT_SHIFT) == glfw.PRESS or
                glfw.get_key(self.win, glfw.KEY_RIGHT_SHIFT) == glfw.PRESS):
                self.draw_boxes_for_all = not self.draw_boxes_for_all
            else:
                self.draw_faces = not self.draw_faces
        elif key == glfw.KEY_C:
            self.color_mode = 1 - self.color_mode
            if self.color_mode == 0: self.set_colors(self.colors_base)
            else: self.set_uniform_color(self.uniform_color)
        elif key == glfw.KEY_LEFT_BRACKET:   self._resize_replicas_3d(-1)
        elif key == glfw.KEY_RIGHT_BRACKET:  self._resize_replicas_3d(+1)
        elif key == glfw.KEY_COMMA:          self._resize_replicas_xy(-1)
        elif key == glfw.KEY_PERIOD:         self._resize_replicas_xy(+1)
        elif key == glfw.KEY_T:              self.keep_view = not self.keep_view
        elif key == glfw.KEY_G:              self.goto_mode = True; self._goto_buf = ""; self._flash_title("Goto index: ")
        elif key == glfw.KEY_LEFT:           self._step(-1)
        elif key == glfw.KEY_RIGHT:          self._step(+1)
        elif key == glfw.KEY_PAGE_UP:        self._step(-10)
        elif key == glfw.KEY_PAGE_DOWN:      self._step(+10)
        elif key == glfw.KEY_HOME:           self._load_index(0)
        elif key == glfw.KEY_END:            self._load_index(len(self.provider)-1)

        # --- auto play ---
        elif key == glfw.KEY_A:
            self.autoplay_on = not self.autoplay_on
            status = "ON" if self.autoplay_on else "OFF"
            print(f"[viewer] Autoplay {status}. Rate: {self.frames_per_second:.1f} FPS")
        elif key == glfw.KEY_EQUAL or key == glfw.KEY_KP_ADD: # Tecla '+' o KP '+'
            self.frames_per_second = min(1000.0, self.frames_per_second + 5.0)
            print(f"[viewer] Autoplay rate set to {self.frames_per_second:.1f} FPS")
        elif key == glfw.KEY_MINUS or key == glfw.KEY_KP_SUBTRACT: # Tecla '-' o KP '-'
            self.frames_per_second = max(0.5, self.frames_per_second - 5.0)
            print(f"[viewer] Autoplay rate set to {self.frames_per_second:.1f} FPS")
        # ----------------------------------------------------

        elif key == glfw.KEY_E:
            self.show_energy_plot = not self.show_energy_plot
        elif key == glfw.KEY_S:
            if not self.sorted_by_energy:
                self._sort_by_energy()
            else:
                self._unsort()

    # ----- helpers -----
    def _flash_title(self, extra=""):
        glfw.set_window_title(self.win, f"[{self.index+1}/{len(self.provider)}] Energy: {self.energy:.6f} eV | Atoms: {self.N}  {extra}")

    def _reset_camera(self):
        mn, mx = compute_bounds(np.vstack([self.pos, cell_corners(self.lat)]))
        center = (mn + mx) * 0.5; diag = float(np.linalg.norm(mx - mn))
        self.cam.center = center.astype(np.float32)
        self.cam.offset = np.array([1.8*diag, 1.2*diag, 0.9*diag], dtype=np.float32)
        self.cam.yaw_v = self.cam.pitch_v = self.cam.zoom_v = 0.0; self.cam.pan_v[:] = 0.0

    '''
    def _step(self, delta):
        idx = (self.index + delta) % len(self.provider)
        self._load_index(idx)
    '''
    def _step(self, delta):
        n = len(self.sorted_indices)
        idx = (self.index + delta) % n
        self._load_index(idx)
    '''
    def _load_index(self, idx: int):
        # store current view parameters if keep_view
        old_center = self.cam.center.copy() if hasattr(self, 'cam') else None
        old_offset = self.cam.offset.copy() if hasattr(self, 'cam') else None

        positions, lattice, energy, elements, colors, radii = self.provider.get(idx)
        self._ingest_structure(positions, lattice, energy, elements, colors, radii)
        self._upload_atom_tbos()
        self._build_cell_buffers()
        self._rebuild_replica_offsets()
        self.index = idx

        if self.keep_view and old_center is not None and old_offset is not None:
            # preserve orientation+distance; just keep offset vector and recenter already done
            pass
    '''
    def _load_index(self, idx: int):
        idx = int(idx)
        real_idx = self.sorted_indices[idx]  # map to true dataset index
        positions, lattice, energy, elements, colors, radii = self.provider.get(real_idx)
        self._ingest_structure(positions, lattice, energy, elements, colors, radii)
        self._upload_atom_tbos()
        self._build_cell_buffers()
        self._rebuild_replica_offsets()
        self.index = idx

    def _resize_replicas_3d(self, delta: int):
        rx, ry, rz = self.replicas
        r = max(0, min(100, max(rx, ry, rz) + delta))
        self.replicas = (r, r, r); self._rebuild_replica_offsets()

    def _resize_replicas_xy(self, delta: int):
        rx, ry, rz = self.replicas
        rxy = max(0, min(100, max(rx, ry) + delta))
        self.replicas = (rxy, rxy, rz); self._rebuild_replica_offsets()

    # ----- Color API -----
    def set_colors(self, colors: np.ndarray):
        colors = np.asarray(colors, dtype=np.float32).reshape(self.N,3)
        self.colors_current = colors.copy()
        self._update_color_tbo()

    def set_uniform_color(self, rgb: Tuple[float,float,float]):
        arr = np.tile(np.array(rgb, dtype=np.float32), (self.N,1))
        self.set_colors(arr)

    # ----- Screenshot -----
    def _save_screenshot(self):
        w, h = glfw.get_framebuffer_size(self.win)
        pixels = glReadPixels(0, 0, w, h, GL_RGBA, GL_UNSIGNED_BYTE)
        img = np.frombuffer(pixels, dtype=np.uint8).reshape(h, w, 4); img = np.flipud(img)
        ts = time.strftime("%Y%m%d_%H%M%S"); base = f"screenshot_{ts}_idx{self.index+1}"
        try:
            from PIL import Image; Image.fromarray(img, mode='RGBA').save(base+'.png'); fname=base+'.png'
        except Exception:
            try:
                import imageio.v2 as imageio; imageio.imwrite(base+'.png', img); fname=base+'.png'
            except Exception:
                rgb = img[:,:,:3]; fname=base+'.ppm'
                with open(fname,'wb') as f: f.write(f'P6\n{w} {h}\n255\n'.encode('ascii')); f.write(rgb.tobytes())
        print('[saved]', os.path.abspath(fname))

    # ----- Main loop -----
    def loop(self):
        prev = time.perf_counter()
        while not glfw.window_should_close(self.win):
            now = time.perf_counter(); dt = max(1e-6, now - prev); prev = now

            # --- auto play ---
            if self.autoplay_on:
                self._time_since_last_frame += dt
                frame_time = 1.0 / self.frames_per_second
                if self._time_since_last_frame >= frame_time:
                    steps = int(self._time_since_last_frame / frame_time)
                    self._step(steps)
                    self._time_since_last_frame %= frame_time # Reiniciar el exceso de tiempo
            # -------------------------------------------

            # Camera
            if abs(self.cam.yaw_v)>1e-6: self.cam.rotate_yaw(self.cam.yaw_v); self.cam.yaw_v *= 0.85
            if abs(self.cam.pitch_v)>1e-6: self.cam.rotate_pitch(self.cam.pitch_v); self.cam.pitch_v *= 0.85
            self.cam.offset *= math.exp(self.cam.zoom_v * dt); self.cam.zoom_v *= 0.80

            # Pan
            w, h = glfw.get_framebuffer_size(self.win)
            px_to_world = 2.0 * np.linalg.norm(self.cam.offset) * math.tan(math.radians(self.cam.fov*0.5)) / max(1.0, h)
            right = self.cam.right(); up = normalize(np.cross(right, self.cam.forward()))
            self.cam.center += (-self.cam.pan_v[0] * px_to_world) * right + (self.cam.pan_v[1] * px_to_world) * up
            self.cam.pan_v *= 0.80

            # Matrices
            eye = self.cam.eye()
            view = look_at(eye, self.cam.center, WORLD_UP)
            near = 0.05; far = max(1000.0, np.linalg.norm(self.cam.offset)*5.0)
            aspect = (w if w>0 else 1) / (h if h>0 else 1)
            proj = perspective(self.cam.fov, aspect, near, far)

            glViewport(0,0,w,h); glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

            # Faces (central only, optional)
            if self.draw_faces and self.face_count>0:
                glEnable(GL_BLEND); glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA); glDepthMask(GL_FALSE)
                glUseProgram(self.line_prog)
                glUniformMatrix4fv(glGetUniformLocation(self.line_prog,"uView"),1,GL_FALSE,view.T)
                glUniformMatrix4fv(glGetUniformLocation(self.line_prog,"uProj"),1,GL_FALSE,proj.T)
                glUniform4f(glGetUniformLocation(self.line_prog,"uRGBA"), 1.0,1.0,1.0,0.08)
                glBindVertexArray(self.face_vao); glDrawArrays(GL_TRIANGLES, 0, self.face_count); glBindVertexArray(0)
                glDepthMask(GL_TRUE); glDisable(GL_BLEND)

            # Spheres: instanced over atoms x replicas
            glUseProgram(self.sphere_prog)
            glUniformMatrix4fv(glGetUniformLocation(self.sphere_prog,"uView"),1,GL_FALSE,view.T)
            glUniformMatrix4fv(glGetUniformLocation(self.sphere_prog,"uProj"),1,GL_FALSE,proj.T)
            glUniform3f(glGetUniformLocation(self.sphere_prog,"uLightDirVS"),0.4,0.6,0.7)
            glUniform1i(glGetUniformLocation(self.sphere_prog,"uAtomCount"), self.N)
            glUniform1i(glGetUniformLocation(self.sphere_prog,"uColorMode"), self.color_mode)
            glUniform3f(glGetUniformLocation(self.sphere_prog,"uUniformColor"),
                        float(self.uniform_color[0]), float(self.uniform_color[1]), float(self.uniform_color[2]))
            glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_BUFFER, self.pr_tbo)
            glActiveTexture(GL_TEXTURE1); glBindTexture(GL_TEXTURE_BUFFER, self.col_tbo)
            glActiveTexture(GL_TEXTURE2); glBindTexture(GL_TEXTURE_BUFFER, self.rep_tbo)
            glUniform1i(glGetUniformLocation(self.sphere_prog,"uAtomPosRad"), 0)
            glUniform1i(glGetUniformLocation(self.sphere_prog,"uAtomColor"), 1)
            glUniform1i(glGetUniformLocation(self.sphere_prog,"uReplicaOffsets"), 2)
            glBindVertexArray(self.quad_vao)
            glDrawArraysInstanced(GL_TRIANGLE_STRIP, 0, 4, self.N * len(self.replica_offsets))
            glBindVertexArray(0)

            # Lattice lines: per-replica instancing (or central only)
            glUseProgram(self.line_prog)
            glUniformMatrix4fv(glGetUniformLocation(self.line_prog,"uView"),1,GL_FALSE,view.T)
            glUniformMatrix4fv(glGetUniformLocation(self.line_prog,"uProj"),1,GL_FALSE,proj.T)
            glUniform4f(glGetUniformLocation(self.line_prog,"uRGBA"), 1.0,1.0,1.0,1.0)
            glActiveTexture(GL_TEXTURE0); glBindTexture(GL_TEXTURE_BUFFER, self.rep_tbo)
            glUniform1i(glGetUniformLocation(self.line_prog,"uReplicaOffsets"), 0)
            glBindVertexArray(self.cell_vao); safe_gl_line_width(1.0)
            reps_to_draw = len(self.replica_offsets) if self.draw_boxes_for_all else 1
            glDrawArraysInstanced(GL_LINES, 0, self.cell_count, reps_to_draw)
            glBindVertexArray(0)

            self._draw_energy_plot()

            glfw.swap_buffers(self.win); glfw.poll_events()
        glfw.terminate()

# ---------- Public API ----------
def browse_structures(provider: StructureProvider,
                      start_index: int = 0,
                      replicas: Tuple[int,int,int] = (0,0,0),
                      draw_boxes_for_all: bool = False,
                      uniform_color: Optional[Tuple[float,float,float]] = None,
                      palette: Optional[Dict[str, Tuple[float,float,float]]] = None,
                      keep_view: bool = False,
                      window_size=(1280, 800)) -> None:
    viewer = Viewer(provider, start_index=start_index,
                    replicas=replicas, draw_boxes_for_all=draw_boxes_for_all,
                    uniform_color=uniform_color, palette=palette,
                    keep_view=keep_view, win_size=window_size)
    viewer.loop()


# ---------- Demo ----------
def _demo_with_partition():
    from sage_lib.partition.Partition import Partition
    path_A = '/Users/dimitry/Documents/Data/EZGA/9-superhero/database/data_base/end_8_4_1'
    path = '/Users/dimitry/Documents/Data/EZGA/9-superhero/hybrid_db/merge_test/new19'
    path = '/Users/dimitry/Documents/Data/EZGA/1_diversity_NiO/runs/ni_o_diversity/supercell_4_4_4'
    p = Partition(storage='hybrid',
                  local_root=path)
    #p.read_files('/Users/dimitry/Documents/Data/Arthem/c.traj')
    provider = PartitionProvider(p)
    # start on #0, browse with arrows
    browse_structures(provider, start_index=0, replicas=(0,0,0), draw_boxes_for_all=False)

if __name__ == "__main__":
    _demo_with_partition()
