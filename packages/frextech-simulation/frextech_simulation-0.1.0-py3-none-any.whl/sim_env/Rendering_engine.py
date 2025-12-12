"""
Complete 3D Rendering Engine with Pygame and OpenGL
Advanced rendering system with multiple techniques, lighting, shadows, and post-processing
"""

import pygame
import numpy as np
import glm
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
from OpenGL.GL.EXT.framebuffer_object import *
import math
import time
from typing import Dict, List, Any, Optional, Tuple
import random

class ShaderManager:
    """Advanced shader management system with hot-reloading"""
    
    def __init__(self):
        self.shaders = {}
        self.shader_files = {}
        self.last_modified_times = {}
        
    def load_shader(self, name: str, vertex_path: str, fragment_path: str, geometry_path: str = None):
        """Load and compile shader with file monitoring"""
        try:
            # Read shader files
            with open(vertex_path, 'r') as f:
                vertex_source = f.read()
            with open(fragment_path, 'r') as f:
                fragment_source = f.read()
                
            geometry_source = None
            if geometry_path:
                with open(geometry_path, 'r') as f:
                    geometry_source = f.read()
                    
            # Compile shader
            shader_program = self.compile_shader_program(vertex_source, fragment_source, geometry_source)
            self.shaders[name] = shader_program
            self.shader_files[name] = (vertex_path, fragment_path, geometry_path)
            self.last_modified_times[name] = self.get_shader_mtime(name)
            
            print(f"Loaded shader: {name}")
            return shader_program
            
        except Exception as e:
            print(f"Error loading shader {name}: {e}")
            return None
            
    def compile_shader_program(self, vertex_source: str, fragment_source: str, geometry_source: str = None):
        """Compile shader program from source code"""
        vertex_shader = compileShader(vertex_source, GL_VERTEX_SHADER)
        fragment_shader = compileShader(fragment_source, GL_FRAGMENT_SHADER)
        
        shaders = [vertex_shader, fragment_shader]
        
        if geometry_source:
            geometry_shader = compileShader(geometry_source, GL_GEOMETRY_SHADER)
            shaders.append(geometry_shader)
            
        return compileProgram(*shaders)
        
    def get_shader_mtime(self, name: str) -> float:
        """Get maximum modification time of shader files"""
        if name not in self.shader_files:
            return 0
            
        vertex_path, fragment_path, geometry_path = self.shader_files[name]
        times = []
        
        for path in [vertex_path, fragment_path, geometry_path]:
            if path and os.path.exists(path):
                times.append(os.path.getmtime(path))
                
        return max(times) if times else 0
        
    def check_reload(self):
        """Check if shaders need reloading (for development)"""
        for name in list(self.shaders.keys()):
            current_mtime = self.get_shader_mtime(name)
            if current_mtime > self.last_modified_times.get(name, 0):
                print(f"Reloading shader: {name}")
                self.load_shader(name, *self.shader_files[name])
                
    def get_shader(self, name: str):
        """Get shader program by name"""
        return self.shaders.get(name)
        
    def set_uniform(self, shader_name: str, uniform_name: str, value):
        """Set uniform value for shader"""
        shader = self.get_shader(shader_name)
        if shader:
            glUseProgram(shader)
            location = glGetUniformLocation(shader, uniform_name)
            
            if location != -1:
                if isinstance(value, (int, bool)):
                    glUniform1i(location, value)
                elif isinstance(value, float):
                    glUniform1f(location, value)
                elif isinstance(value, glm.vec2):
                    glUniform2f(location, value.x, value.y)
                elif isinstance(value, glm.vec3):
                    glUniform3f(location, value.x, value.y, value.z)
                elif isinstance(value, glm.vec4):
                    glUniform4f(location, value.x, value.y, value.z, value.w)
                elif isinstance(value, glm.mat4):
                    glUniformMatrix4fv(location, 1, GL_FALSE, glm.value_ptr(value))
                    
            glUseProgram(0)

class Camera:
    """Advanced 3D camera system with multiple projection modes"""
    
    def __init__(self):
        self.position = glm.vec3(0, 0, 5)
        self.target = glm.vec3(0, 0, 0)
        self.up = glm.vec3(0, 1, 0)
        self.right = glm.vec3(1, 0, 0)
        
        # Camera parameters
        self.fov = 45.0
        self.aspect_ratio = 16.0 / 9.0
        self.near_plane = 0.1
        self.far_plane = 100.0
        
        # Camera control
        self.yaw = -90.0
        self.pitch = 0.0
        self.movement_speed = 5.0
        self.mouse_sensitivity = 0.1
        self.zoom = 45.0
        
        # Camera modes
        self.projection_mode = "perspective"  # "perspective", "orthographic"
        self.ortho_size = 5.0
        
        # Camera state
        self.frustum_planes = []
        self.view_matrix = glm.mat4(1.0)
        self.projection_matrix = glm.mat4(1.0)
        
        self.update_vectors()
        
    def update_vectors(self):
        """Update camera vectors based on yaw and pitch"""
        # Calculate front vector
        front = glm.vec3()
        front.x = math.cos(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        front.y = math.sin(glm.radians(self.pitch))
        front.z = math.sin(glm.radians(self.yaw)) * math.cos(glm.radians(self.pitch))
        
        self.front = glm.normalize(front)
        self.right = glm.normalize(glm.cross(self.front, glm.vec3(0, 1, 0)))
        self.up = glm.normalize(glm.cross(self.right, self.front))
        
    def get_view_matrix(self) -> glm.mat4:
        """Get view matrix"""
        return glm.lookAt(self.position, self.position + self.front, self.up)
        
    def get_projection_matrix(self) -> glm.mat4:
        """Get projection matrix based on current mode"""
        if self.projection_mode == "perspective":
            return glm.perspective(glm.radians(self.fov), self.aspect_ratio, self.near_plane, self.far_plane)
        else:  # orthographic
            return glm.ortho(
                -self.ortho_size * self.aspect_ratio,
                self.ortho_size * self.aspect_ratio,
                -self.ortho_size,
                self.ortho_size,
                self.near_plane,
                self.far_plane
            )
            
    def process_keyboard(self, direction: str, delta_time: float):
        """Process keyboard input for camera movement"""
        velocity = self.movement_speed * delta_time
        
        if direction == "FORWARD":
            self.position += self.front * velocity
        if direction == "BACKWARD":
            self.position -= self.front * velocity
        if direction == "LEFT":
            self.position -= self.right * velocity
        if direction == "RIGHT":
            self.position += self.right * velocity
        if direction == "UP":
            self.position += self.up * velocity
        if direction == "DOWN":
            self.position -= self.up * velocity
            
    def process_mouse_movement(self, xoffset: float, yoffset: float, constrain_pitch: bool = True):
        """Process mouse movement for camera rotation"""
        xoffset *= self.mouse_sensitivity
        yoffset *= self.mouse_sensitivity
        
        self.yaw += xoffset
        self.pitch += yoffset
        
        # Constrain pitch to avoid flip
        if constrain_pitch:
            self.pitch = max(-89.0, min(89.0, self.pitch))
            
        self.update_vectors()
        
    def process_mouse_scroll(self, yoffset: float):
        """Process mouse scroll for zoom"""
        self.zoom -= yoffset
        self.zoom = max(1.0, min(45.0, self.zoom))
        self.fov = self.zoom
        
    def update_frustum(self):
        """Update view frustum for culling"""
        view_proj = self.projection_matrix * self.view_matrix
        self.frustum_planes = self.extract_frustum_planes(view_proj)
        
    def extract_frustum_planes(self, matrix: glm.mat4) -> List[glm.vec4]:
        """Extract frustum planes from view-projection matrix"""
        planes = []
        
        # Extract rows
        rows = [
            glm.vec4(matrix[0][0], matrix[1][0], matrix[2][0], matrix[3][0]),
            glm.vec4(matrix[0][1], matrix[1][1], matrix[2][1], matrix[3][1]),
            glm.vec4(matrix[0][2], matrix[1][2], matrix[2][2], matrix[3][2]),
            glm.vec4(matrix[0][3], matrix[1][3], matrix[2][3], matrix[3][3])
        ]
        
        # Left, Right, Bottom, Top, Near, Far planes
        planes.append(rows[3] + rows[0])  # Left
        planes.append(rows[3] - rows[0])  # Right
        planes.append(rows[3] + rows[1])  # Bottom
        planes.append(rows[3] - rows[1])  # Top
        planes.append(rows[3] + rows[2])  # Near
        planes.append(rows[3] - rows[2])  # Far
        
        # Normalize planes
        for i in range(6):
            length = glm.length(glm.vec3(planes[i]))
            planes[i] /= length
            
        return planes
        
    def is_sphere_in_frustum(self, center: glm.vec3, radius: float) -> bool:
        """Check if sphere is in view frustum"""
        for plane in self.frustum_planes:
            distance = glm.dot(glm.vec3(plane), center) + plane.w
            if distance < -radius:
                return False
        return True

class LightingSystem:
    """Advanced lighting system with multiple light types and shadows"""
    
    def __init__(self):
        self.lights = []
        self.ambient_light = glm.vec3(0.1, 0.1, 0.1)
        self.shadow_maps = {}
        self.shadow_resolution = 1024
        
    def add_directional_light(self, direction: glm.vec3, color: glm.vec3 = None, intensity: float = 1.0):
        """Add directional light"""
        if color is None:
            color = glm.vec3(1.0, 1.0, 1.0)
            
        light = {
            'type': 'directional',
            'direction': glm.normalize(direction),
            'color': color,
            'intensity': intensity,
            'casts_shadows': True
        }
        self.lights.append(light)
        
        if light['casts_shadows']:
            self.create_shadow_map(light)
            
        return light
        
    def add_point_light(self, position: glm.vec3, color: glm.vec3 = None, intensity: float = 1.0, 
                       attenuation: glm.vec3 = None):
        """Add point light"""
        if color is None:
            color = glm.vec3(1.0, 1.0, 1.0)
        if attenuation is None:
            attenuation = glm.vec3(1.0, 0.09, 0.032)  # Default attenuation
            
        light = {
            'type': 'point',
            'position': position,
            'color': color,
            'intensity': intensity,
            'attenuation': attenuation,
            'casts_shadows': False  # Point light shadows are complex
        }
        self.lights.append(light)
        return light
        
    def add_spot_light(self, position: glm.vec3, direction: glm.vec3, color: glm.vec3 = None,
                      intensity: float = 1.0, cut_off: float = 12.5, outer_cut_off: float = 15.0):
        """Add spot light"""
        if color is None:
            color = glm.vec3(1.0, 1.0, 1.0)
            
        light = {
            'type': 'spot',
            'position': position,
            'direction': glm.normalize(direction),
            'color': color,
            'intensity': intensity,
            'cut_off': math.cos(glm.radians(cut_off)),
            'outer_cut_off': math.cos(glm.radians(outer_cut_off)),
            'casts_shadows': True
        }
        self.lights.append(light)
        
        if light['casts_shadows']:
            self.create_shadow_map(light)
            
        return light
        
    def create_shadow_map(self, light):
        """Create shadow map for light"""
        if light['type'] == 'directional':
            # Create depth texture for directional shadow mapping
            shadow_fbo = glGenFramebuffers(1)
            shadow_texture = glGenTextures(1)
            
            glBindTexture(GL_TEXTURE_2D, shadow_texture)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_DEPTH_COMPONENT, 
                        self.shadow_resolution, self.shadow_resolution, 0,
                        GL_DEPTH_COMPONENT, GL_FLOAT, None)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_BORDER)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_BORDER)
            
            border_color = [1.0, 1.0, 1.0, 1.0]
            glTexParameterfv(GL_TEXTURE_2D, GL_TEXTURE_BORDER_COLOR, border_color)
            
            glBindFramebuffer(GL_FRAMEBUFFER, shadow_fbo)
            glFramebufferTexture2D(GL_FRAMEBUFFER, GL_DEPTH_ATTACHMENT, GL_TEXTURE_2D, shadow_texture, 0)
            glDrawBuffer(GL_NONE)
            glReadBuffer(GL_NONE)
            glBindFramebuffer(GL_FRAMEBUFFER, 0)
            
            self.shadow_maps[id(light)] = {
                'fbo': shadow_fbo,
                'texture': shadow_texture,
                'light_space_matrix': glm.mat4(1.0)
            }
            
    def update_shadow_maps(self, camera: Camera):
        """Update shadow maps for current scene"""
        for light in self.lights:
            if light['casts_shadows'] and id(light) in self.shadow_maps:
                self.render_shadow_map(light, camera)
                
    def render_shadow_map(self, light, camera: Camera):
        """Render shadow map for a specific light"""
        shadow_data = self.shadow_maps[id(light)]
        
        if light['type'] == 'directional':
            # Calculate light space matrix for directional light
            light_proj = glm.ortho(-10.0, 10.0, -10.0, 10.0, 1.0, 20.0)
            light_view = glm.lookAt(
                -light['direction'] * 10.0,  # Light position
                glm.vec3(0, 0, 0),           # Look at origin
                glm.vec3(0, 1, 0)            # Up vector
            )
            shadow_data['light_space_matrix'] = light_proj * light_view
            
        # Bind shadow FBO and render depth
        glBindFramebuffer(GL_FRAMEBUFFER, shadow_data['fbo'])
        glViewport(0, 0, self.shadow_resolution, self.shadow_resolution)
        glClear(GL_DEPTH_BUFFER_BIT)
        
        # Here we would render the scene from light's perspective
        # This is simplified - actual implementation would render all shadow-casting objects
        
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
    def set_light_uniforms(self, shader_program: int):
        """Set light uniforms for shader"""
        glUseProgram(shader_program)
        
        # Set ambient light
        glUniform3f(glGetUniformLocation(shader_program, "ambientLight"), 
                   self.ambient_light.x, self.ambient_light.y, self.ambient_light.z)
        
        # Set directional lights
        directional_count = 0
        point_count = 0
        spot_count = 0
        
        for i, light in enumerate(self.lights):
            if light['type'] == 'directional' and directional_count < 4:
                prefix = f"directionalLights[{directional_count}]"
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.direction"),
                           light['direction'].x, light['direction'].y, light['direction'].z)
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.color"),
                           light['color'].x, light['color'].y, light['color'].z)
                glUniform1f(glGetUniformLocation(shader_program, f"{prefix}.intensity"), light['intensity'])
                directional_count += 1
                
            elif light['type'] == 'point' and point_count < 8:
                prefix = f"pointLights[{point_count}]"
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.position"),
                           light['position'].x, light['position'].y, light['position'].z)
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.color"),
                           light['color'].x, light['color'].y, light['color'].z)
                glUniform1f(glGetUniformLocation(shader_program, f"{prefix}.intensity"), light['intensity'])
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.attenuation"),
                           light['attenuation'].x, light['attenuation'].y, light['attenuation'].z)
                point_count += 1
                
            elif light['type'] == 'spot' and spot_count < 4:
                prefix = f"spotLights[{spot_count}]"
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.position"),
                           light['position'].x, light['position'].y, light['position'].z)
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.direction"),
                           light['direction'].x, light['direction'].y, light['direction'].z)
                glUniform3f(glGetUniformLocation(shader_program, f"{prefix}.color"),
                           light['color'].x, light['color'].y, light['color'].z)
                glUniform1f(glGetUniformLocation(shader_program, f"{prefix}.intensity"), light['intensity'])
                glUniform1f(glGetUniformLocation(shader_program, f"{prefix}.cutOff"), light['cut_off'])
                glUniform1f(glGetUniformLocation(shader_program, f"{prefix}.outerCutOff"), light['outer_cut_off'])
                spot_count += 1
                
        # Set light counts
        glUniform1i(glGetUniformLocation(shader_program, "directionalLightCount"), directional_count)
        glUniform1i(glGetUniformLocation(shader_program, "pointLightCount"), point_count)
        glUniform1i(glGetUniformLocation(shader_program, "spotLightCount"), spot_count)
        
        glUseProgram(0)

class PostProcessing:
    """Advanced post-processing effects system"""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.effects = {}
        self.framebuffers = {}
        self.textures = {}
        
        # Create main framebuffer
        self.create_framebuffer("main", width, height)
        
        # Initialize effects
        self.setup_effects()
        
    def create_framebuffer(self, name: str, width: int, height: int):
        """Create framebuffer with color and depth attachments"""
        # Generate framebuffer
        fbo = glGenFramebuffers(1)
        glBindFramebuffer(GL_FRAMEBUFFER, fbo)
        
        # Create color texture
        color_texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, color_texture)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, None)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glFramebufferTexture2D(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_TEXTURE_2D, color_texture, 0)
        
        # Create depth/stencil buffer
        rbo = glGenRenderbuffers(1)
        glBindRenderbuffer(GL_RENDERBUFFER, rbo)
        glRenderbufferStorage(GL_RENDERBUFFER, GL_DEPTH24_STENCIL8, width, height)
        glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_DEPTH_STENCIL_ATTACHMENT, GL_RENDERBUFFER, rbo)
        
        # Check framebuffer completeness
        if glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE:
            print(f"Framebuffer {name} not complete!")
            
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        
        self.framebuffers[name] = fbo
        self.textures[name] = color_texture
        
        return fbo, color_texture
        
    def setup_effects(self):
        """Setup post-processing effects"""
        self.effects = {
            'bloom': {
                'enabled': False,
                'threshold': 0.7,
                'intensity': 1.0
            },
            'motion_blur': {
                'enabled': False,
                'intensity': 0.5
            },
            'color_correction': {
                'enabled': False,
                'brightness': 1.0,
                'contrast': 1.0,
                'saturation': 1.0
            },
            'vignette': {
                'enabled': False,
                'intensity': 0.5,
                'radius': 0.8
            },
            'chromatic_aberration': {
                'enabled': False,
                'offset': 0.005
            }
        }
        
    def begin_frame(self):
        """Begin rendering to framebuffer"""
        glBindFramebuffer(GL_FRAMEBUFFER, self.framebuffers['main'])
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
    def end_frame(self):
        """End rendering to framebuffer and apply post-processing"""
        glBindFramebuffer(GL_FRAMEBUFFER, 0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Apply post-processing effects
        self.apply_effects()
        
    def apply_effects(self):
        """Apply all enabled post-processing effects"""
        # This would implement the actual post-processing pipeline
        # For now, just render the main texture to screen
        glBindTexture(GL_TEXTURE_2D, self.textures['main'])
        
        # Simple fullscreen quad rendering
        glBegin(GL_QUADS)
        glTexCoord2f(0, 0); glVertex2f(-1, -1)
        glTexCoord2f(1, 0); glVertex2f(1, -1)
        glTexCoord2f(1, 1); glVertex2f(1, 1)
        glTexCoord2f(0, 1); glVertex2f(-1, 1)
        glEnd()

class Mesh:
    """3D mesh with vertex data and rendering capabilities"""
    
    def __init__(self):
        self.vertices = []
        self.normals = []
        self.texcoords = []
        self.colors = []
        self.indices = []
        
        self.vao = 0
        self.vbo = 0
        self.ebo = 0
        self.vertex_count = 0
        
        self.material = {
            'diffuse': glm.vec3(0.8, 0.8, 0.8),
            'specular': glm.vec3(0.5, 0.5, 0.5),
            'shininess': 32.0
        }
        
    def create_cube(self, size: float = 1.0):
        """Create a cube mesh"""
        s = size / 2.0
        
        # Define cube vertices (position, normal, texcoord)
        vertices = [
            # Front face
            [-s, -s, s, 0, 0, 1, 0, 0], [s, -s, s, 0, 0, 1, 1, 0], [s, s, s, 0, 0, 1, 1, 1], [-s, s, s, 0, 0, 1, 0, 1],
            # Back face
            [-s, -s, -s, 0, 0, -1, 1, 0], [-s, s, -s, 0, 0, -1, 1, 1], [s, s, -s, 0, 0, -1, 0, 1], [s, -s, -s, 0, 0, -1, 0, 0],
            # Top face
            [-s, s, -s, 0, 1, 0, 0, 1], [-s, s, s, 0, 1, 0, 0, 0], [s, s, s, 0, 1, 0, 1, 0], [s, s, -s, 0, 1, 0, 1, 1],
            # Bottom face
            [-s, -s, -s, 0, -1, 0, 1, 1], [s, -s, -s, 0, -1, 0, 0, 1], [s, -s, s, 0, -1, 0, 0, 0], [-s, -s, s, 0, -1, 0, 1, 0],
            # Right face
            [s, -s, -s, 1, 0, 0, 1, 0], [s, s, -s, 1, 0, 0, 1, 1], [s, s, s, 1, 0, 0, 0, 1], [s, -s, s, 1, 0, 0, 0, 0],
            # Left face
            [-s, -s, -s, -1, 0, 0, 0, 0], [-s, -s, s, -1, 0, 0, 1, 0], [-s, s, s, -1, 0, 0, 1, 1], [-s, s, -s, -1, 0, 0, 0, 1]
        ]
        
        # Define indices
        indices = [
            0, 1, 2, 2, 3, 0,      # Front
            4, 5, 6, 6, 7, 4,      # Back
            8, 9, 10, 10, 11, 8,   # Top
            12, 13, 14, 14, 15, 12,# Bottom
            16, 17, 18, 18, 19, 16,# Right
            20, 21, 22, 22, 23, 20 # Left
        ]
        
        self.vertices = vertices
        self.indices = indices
        self.vertex_count = len(indices)
        
        self.upload_to_gpu()
        
    def create_sphere(self, radius: float = 1.0, segments: int = 16):
        """Create a sphere mesh"""
        vertices = []
        indices = []
        
        for i in range(segments + 1):
            lat0 = math.pi * (-0.5 + float(i - 1) / segments)
            z0 = math.sin(lat0)
            zr0 = math.cos(lat0)
            
            lat1 = math.pi * (-0.5 + float(i) / segments)
            z1 = math.sin(lat1)
            zr1 = math.cos(lat1)
            
            for j in range(segments + 1):
                lng = 2 * math.pi * float(j - 1) / segments
                x = math.cos(lng)
                y = math.sin(lng)
                
                # Vertex 1
                vertices.extend([x * zr0 * radius, y * zr0 * radius, z0 * radius, x, y, z0, j/segments, i/segments])
                # Vertex 2  
                vertices.extend([x * zr1 * radius, y * zr1 * radius, z1 * radius, x, y, z1, j/segments, (i+1)/segments])
                
        # Generate indices
        for i in range(segments):
            for j in range(segments):
                first = (i * (segments + 1)) + j
                second = first + segments + 1
                
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])
                
        self.vertices = vertices
        self.indices = indices
        self.vertex_count = len(indices)
        
        self.upload_to_gpu()
        
    def upload_to_gpu(self):
        """Upload mesh data to GPU"""
        if not self.vertices or not self.indices:
            return
            
        # Generate buffers
        self.vao = glGenVertexArrays(1)
        self.vbo = glGenBuffers(1)
        self.ebo = glGenBuffers(1)
        
        glBindVertexArray(self.vao)
        
        # Upload vertex data
        vertex_data = np.array(self.vertices, dtype=np.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.vbo)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
        
        # Upload index data
        index_data = np.array(self.indices, dtype=np.uint32)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.ebo)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)
        
        # Set vertex attributes
        # Position (3), Normal (3), TexCoord (2)
        stride = 8 * sizeof(GLfloat)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(0))
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(1, 3, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(3 * sizeof(GLfloat)))
        glEnableVertexAttribArray(1)
        glVertexAttribPointer(2, 2, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(6 * sizeof(GLfloat)))
        glEnableVertexAttribArray(2)
        
        glBindVertexArray(0)
        
    def render(self, shader_program: int, model_matrix: glm.mat4):
        """Render the mesh"""
        if self.vao == 0:
            return
            
        glUseProgram(shader_program)
        glBindVertexArray(self.vao)
        
        # Set model matrix
        model_loc = glGetUniformLocation(shader_program, "model")
        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model_matrix))
        
        # Set material properties
        glUniform3f(glGetUniformLocation(shader_program, "material.diffuse"),
                   self.material['diffuse'].x, self.material['diffuse'].y, self.material['diffuse'].z)
        glUniform3f(glGetUniformLocation(shader_program, "material.specular"),
                   self.material['specular'].x, self.material['specular'].y, self.material['specular'].z)
        glUniform1f(glGetUniformLocation(shader_program, "material.shininess"), self.material['shininess'])
        
        # Draw mesh
        glDrawElements(GL_TRIANGLES, self.vertex_count, GL_UNSIGNED_INT, None)
        
        glBindVertexArray(0)
        glUseProgram(0)

class RenderingEngine:
    """Complete 3D rendering engine with advanced features"""
    
    def __init__(self, window_width: int = 1200, window_height: int = 800):
        self.window_width = window_width
        self.window_height = window_height
        
        # Core systems
        self.shader_manager = ShaderManager()
        self.camera = Camera()
        self.lighting_system = LightingSystem()
        self.post_processing = PostProcessing(window_width, window_height)
        
        # Rendering state
        self.render_mode = "solid"  # solid, wireframe, points
        self.enable_lighting = True
        self.enable_shadows = True
        self.enable_fog = False
        self.fog_color = glm.vec3(0.5, 0.5, 0.5)
        self.fog_density = 0.01
        
        # Scene objects
        self.meshes = []
        self.particle_systems = []
        
        # Performance tracking
        self.frame_time = 0.0
        self.triangle_count = 0
        self.draw_calls = 0
        
        # Initialize OpenGL
        self.initialize_opengl()
        
    def initialize_opengl(self):
        """Initialize OpenGL settings and resources"""
        # Basic OpenGL settings
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glCullFace(GL_BACK)
        glFrontFace(GL_CCW)
        
        # Blending for transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        
        # Multisampling for anti-aliasing
        glEnable(GL_MULTISAMPLE)
        
        # Load default shaders
        self.load_default_shaders()
        
        # Setup default lighting
        self.setup_default_lighting()
        
        # Create some default meshes
        self.create_default_meshes()
        
        print("Rendering Engine initialized successfully")
        
    def load_default_shaders(self):
        """Load default shader programs"""
        # Basic phong shader
        phong_vertex = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aNormal;
        layout (location = 2) in vec2 aTexCoord;
        
        out vec3 FragPos;
        out vec3 Normal;
        out vec2 TexCoord;
        
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        void main() {
            FragPos = vec3(model * vec4(aPos, 1.0));
            Normal = mat3(transpose(inverse(model))) * aNormal;
            TexCoord = aTexCoord;
            
            gl_Position = projection * view * vec4(FragPos, 1.0);
        }
        """
        
        phong_fragment = """
        #version 330 core
        in vec3 FragPos;
        in vec3 Normal;
        in vec2 TexCoord;
        
        out vec4 FragColor;
        
        struct Material {
            vec3 diffuse;
            vec3 specular;
            float shininess;
        };
        
        struct DirLight {
            vec3 direction;
            vec3 color;
            float intensity;
        };
        
        uniform Material material;
        uniform DirLight directionalLights[4];
        uniform int directionalLightCount;
        
        uniform vec3 viewPos;
        uniform vec3 ambientLight;
        
        void main() {
            vec3 normal = normalize(Normal);
            vec3 viewDir = normalize(viewPos - FragPos);
            
            // Ambient
            vec3 ambient = ambientLight * material.diffuse;
            
            // Diffuse & Specular
            vec3 lighting = ambient;
            
            for (int i = 0; i < directionalLightCount; i++) {
                // Diffuse
                vec3 lightDir = normalize(-directionalLights[i].direction);
                float diff = max(dot(normal, lightDir), 0.0);
                vec3 diffuse = directionalLights[i].color * diff * material.diffuse * directionalLights[i].intensity;
                
                // Specular
                vec3 reflectDir = reflect(-lightDir, normal);
                float spec = pow(max(dot(viewDir, reflectDir), 0.0), material.shininess);
                vec3 specular = directionalLights[i].color * spec * material.specular * directionalLights[i].intensity;
                
                lighting += diffuse + specular;
            }
            
            FragColor = vec4(lighting, 1.0);
        }
        """
        
        self.shader_manager.shaders['phong'] = self.shader_manager.compile_shader_program(phong_vertex, phong_fragment)
        
        # Simple unlit shader for basic rendering
        simple_vertex = """
        #version 330 core
        layout (location = 0) in vec3 aPos;
        layout (location = 1) in vec3 aColor;
        
        out vec3 fragColor;
        
        uniform mat4 model;
        uniform mat4 view;
        uniform mat4 projection;
        
        void main() {
            gl_Position = projection * view * model * vec4(aPos, 1.0);
            fragColor = aColor;
        }
        """
        
        simple_fragment = """
        #version 330 core
        in vec3 fragColor;
        out vec4 FragColor;
        
        void main() {
            FragColor = vec4(fragColor, 1.0);
        }
        """
        
        self.shader_manager.shaders['simple'] = self.shader_manager.compile_shader_program(simple_vertex, simple_fragment)
        
    def setup_default_lighting(self):
        """Setup default lighting for the scene"""
        # Main directional light (sun)
        self.lighting_system.add_directional_light(
            direction=glm.vec3(-0.5, -1.0, -0.5),
            color=glm.vec3(1.0, 0.95, 0.9),
            intensity=1.2
        )
        
        # Fill light
        self.lighting_system.add_directional_light(
            direction=glm.vec3(0.5, -0.5, 0.5),
            color=glm.vec3(0.3, 0.4, 0.6),
            intensity=0.3
        )
        
        # Some point lights for interest
        self.lighting_system.add_point_light(
            position=glm.vec3(2, 2, 2),
            color=glm.vec3(1.0, 0.5, 0.2),
            intensity=1.5
        )
        
    def create_default_meshes(self):
        """Create some default meshes for testing"""
        # Create a cube mesh
        cube_mesh = Mesh()
        cube_mesh.create_cube(2.0)
        cube_mesh.material = {
            'diffuse': glm.vec3(0.8, 0.3, 0.3),
            'specular': glm.vec3(0.8, 0.8, 0.8),
            'shininess': 32.0
        }
        self.meshes.append(('cube', cube_mesh))
        
        # Create a sphere mesh
        sphere_mesh = Mesh()
        sphere_mesh.create_sphere(1.5, 32)
        sphere_mesh.material = {
            'diffuse': glm.vec3(0.3, 0.3, 0.8),
            'specular': glm.vec3(0.8, 0.8, 0.8),
            'shininess': 64.0
        }
        self.meshes.append(('sphere', sphere_mesh))
        
    def render_frame(self):
        """Render complete frame"""
        start_time = time.time()
        self.draw_calls = 0
        self.triangle_count = 0
        
        # Begin post-processing frame
        self.post_processing.begin_frame()
        
        # Clear screen
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        # Update camera matrices
        self.camera.view_matrix = self.camera.get_view_matrix()
        self.camera.projection_matrix = self.camera.get_projection_matrix()
        self.camera.update_frustum()
        
        # Update shadow maps
        if self.enable_shadows:
            self.lighting_system.update_shadow_maps(self.camera)
            
        # Set render mode
        self.set_render_mode(self.render_mode)
        
        # Render all meshes
        for name, mesh in self.meshes:
            if self.camera.is_sphere_in_frustum(glm.vec3(0, 0, 0), 5.0):  # Simple culling
                model_matrix = glm.mat4(1.0)
                mesh.render(self.shader_manager.get_shader('phong'), model_matrix)
                self.draw_calls += 1
                self.triangle_count += mesh.vertex_count // 3
                
        # Render particle systems
        for particle_system in self.particle_systems:
            particle_system.render(
                self.camera.view_matrix,
                self.camera.projection_matrix,
                self.camera.position
            )
            self.draw_calls += 1
            
        # End post-processing frame
        self.post_processing.end_frame()
        
        self.frame_time = time.time() - start_time
        
    def set_render_mode(self, mode: str):
        """Set polygon rendering mode"""
        if mode == "solid":
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif mode == "wireframe":
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif mode == "points":
            glPolygonMode(GL_FRONT_AND_BACK, GL_POINT)
            
    def add_particle_system(self, particle_system):
        """Add particle system for rendering"""
        self.particle_systems.append(particle_system)
        
    def remove_particle_system(self, particle_system):
        """Remove particle system from rendering"""
        if particle_system in self.particle_systems:
            self.particle_systems.remove(particle_system)
            
    def get_performance_stats(self) -> Dict:
        """Get rendering performance statistics"""
        return {
            'frame_time': self.frame_time,
            'fps': 1.0 / self.frame_time if self.frame_time > 0 else 0,
            'triangle_count': self.triangle_count,
            'draw_calls': self.draw_calls,
            'mesh_count': len(self.meshes),
            'particle_system_count': len(self.particle_systems),
            'light_count': len(self.lighting_system.lights)
        }
        
    def resize(self, width: int, height: int):
        """Handle window resize"""
        self.window_width = width
        self.window_height = height
        self.camera.aspect_ratio = width / height
        glViewport(0, 0, width, height)
        
        # Recreate post-processing framebuffers
        self.post_processing = PostProcessing(width, height)
        
    def cleanup(self):
        """Clean up rendering resources"""
        # Clean up meshes
        for name, mesh in self.meshes:
            if mesh.vao:
                glDeleteVertexArrays(1, [mesh.vao])
            if mesh.vbo:
                glDeleteBuffers(1, [mesh.vbo])
            if mesh.ebo:
                glDeleteBuffers(1, [mesh.ebo])
                
        # Clean up shaders
        for shader in self.shader_manager.shaders.values():
            glDeleteProgram(shader)
            
        # Clean up framebuffers
        for fbo in self.post_processing.framebuffers.values():
            glDeleteFramebuffers(1, [fbo])
        for texture in self.post_processing.textures.values():
            glDeleteTextures(1, [texture])

# Demo and testing
if __name__ == "__main__":
    # Initialize pygame and OpenGL
    pygame.init()
    screen = pygame.display.set_mode((1200, 800), pygame.OPENGL | pygame.DOUBLEBUF)
    pygame.display.set_caption("3D Rendering Engine Test")
    
    # Create rendering engine
    renderer = RenderingEngine(1200, 800)
    
    # Main loop
    running = True
    clock = pygame.time.Clock()
    
    print("Starting 3D rendering test...")
    
    while running:
        dt = clock.tick(60) / 1000.0
        
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    # Toggle render mode
                    modes = ["solid", "wireframe", "points"]
                    current_index = modes.index(renderer.render_mode)
                    renderer.render_mode = modes[(current_index + 1) % len(modes)]
                    print(f"Render mode: {renderer.render_mode}")
                    
        # Update camera (simple rotation for demo)
        renderer.camera.yaw += 20.0 * dt
        renderer.camera.update_vectors()
        
        # Render frame
        renderer.render_frame()
        
        # Update display
        pygame.display.flip()
        
        # Print stats occasionally
        if pygame.time.get_ticks() % 1000 < 16:
            stats = renderer.get_performance_stats()
            print(f"FPS: {stats['fps']:.1f}, Triangles: {stats['triangle_count']}")
            
    # Cleanup
    renderer.cleanup()
    pygame.quit()
    print("3D rendering test completed successfully!")