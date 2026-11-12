import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Configuración de la página
st.set_page_config(page_title="Simulación - Flujo de Poiseuille", layout="wide")

# Título e información
st.title("Simulación Interactiva: Campo Vectorial de Poiseuille")
st.markdown("""
Esta aplicación representa la **Fase 2** del proyecto. Modifica los parámetros en la barra lateral para recalcular dinámicamente 
el campo de velocidades, el caudal total (flujo) y el rotacional en la pared de la tubería, evaluados en la Fase 1.
""")

# --- Barra lateral para parámetros ---
st.sidebar.header("Parámetros del Campo")
R = st.sidebar.slider("Radio de la tubería (R) [m]", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
v_max = st.sidebar.slider("Velocidad máxima (v_max) [m/s]", min_value=0.5, max_value=5.0, value=2.0, step=0.5)

# --- Cálculos dinámicos basados en Fase 1 ---
# Caudal (Flujo) Q = (pi/2) * v_max * R^2
caudal_m3 = (np.pi / 2) * v_max * (R**2)
caudal_L = caudal_m3 * 1000

# Rotacional máximo en la pared (en x=R, y=0) = 2 * v_max / R
rotacional_max = 2 * v_max / R

# Circulación en eje central (z=0 a z=1)
circulacion_central = v_max * 1.0

# --- Métricas (Exhibición de resultados numéricos exigida en la Fase 2) ---
st.subheader("Resultados Analíticos en Vivo")
col1, col2, col3 = st.columns(3)
col1.metric("Caudal (Flujo por la tapa)", f"{caudal_m3:.6f} m³/s", f"{caudal_L:.2f} L/s")
col2.metric("Rotacional en la pared", f"(0, {rotacional_max:.1f}, 0) s⁻¹")
col3.metric("Circulación Eje Central (C1)", f"{circulacion_central:.2f} m²/s")

# --- Gráficas ---
st.subheader("Representaciones del Campo Vectorial")
col_fig1, col_fig2 = st.columns(2)

with col_fig1:
    # Gráfica 2D
    r = np.linspace(0, R, 20)
    theta = np.linspace(0, 2*np.pi, 30)
    r_grid, theta_grid = np.meshgrid(r, theta)
    X = r_grid * np.cos(theta_grid)
    Y = r_grid * np.sin(theta_grid)
    V_z = v_max * (1 - (X**2 + Y**2) / R**2)

    fig2d, ax2d = plt.subplots(figsize=(5, 5))
    c = ax2d.contourf(X, Y, V_z, levels=50, cmap='viridis')
    fig2d.colorbar(c, label='Velocidad $v_z$ (m/s)')
    círculo = plt.Circle((0, 0), R, color='black', fill=False, linewidth=2, linestyle='--')
    ax2d.add_patch(círculo)
    ax2d.set_title('Corte Transversal 2D')
    ax2d.set_xlabel('X (m)')
    ax2d.set_ylabel('Y (m)')
    ax2d.set_aspect('equal')
    st.pyplot(fig2d)

with col_fig2:
    # Gráfica 3D
    x_1d = np.linspace(-R, R, 15)
    y_1d = np.linspace(-R, R, 15)
    X3, Y3 = np.meshgrid(x_1d, y_1d)
    mask = (X3**2 + Y3**2) <= R**2
    X3_v = X3[mask]
    Y3_v = Y3[mask]
    Z3_b = np.zeros_like(X3_v)
    W = v_max * (1 - (X3_v**2 + Y3_v**2) / R**2)
    U = np.zeros_like(X3_v)
    V = np.zeros_like(X3_v)

    fig3d = plt.figure(figsize=(5, 5))
    ax3d = fig3d.add_subplot(111, projection='3d')
    ax3d.quiver(X3_v, Y3_v, Z3_b, U, V, W, length=0.1*v_max, normalize=False, color='blue', alpha=0.7)
    
    theta_c = np.linspace(0, 2*np.pi, 100)
    ax3d.plot(R*np.cos(theta_c), R*np.sin(theta_c), 0, color='black', linewidth=2, linestyle='--')
    ax3d.set_title('Perfil Tridimensional')
    ax3d.set_xlabel('X')
    ax3d.set_ylabel('Y')
    ax3d.set_zlabel('v_z')
    ax3d.set_zlim(0, 5.5)
    st.pyplot(fig3d)
