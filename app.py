import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Simulación - Flujo de Poiseuille", layout="wide")

st.title("Simulación Interactiva: Campo Vectorial de Poiseuille")
st.markdown("""
Esta aplicación representa la **Fase 2** del proyecto. Modifica los parámetros en la barra lateral para recalcular dinámicamente 
el campo de velocidades, el caudal total (flujo) y el rotacional en la pared de la tubería.
""")

st.sidebar.header("Parámetros del Campo")
R = st.sidebar.slider("Radio de la tubería (R) [m]", min_value=0.01, max_value=0.10, value=0.05, step=0.01)
v_max = st.sidebar.slider("Velocidad máxima (v_max) [m/s]", min_value=0.5, max_value=5.0, value=2.0, step=0.5)

caudal_m3 = (np.pi / 2) * v_max * (R**2)
caudal_L = caudal_m3 * 1000
rotacional_max = 2 * v_max / R
circulacion_central = v_max * 1.0

st.subheader("Resultados Analíticos en Vivo")
col1, col2, col3 = st.columns(3)
col1.metric("Caudal (Flujo por la tapa)", f"{caudal_m3:.6f} m³/s", f"{caudal_L:.2f} L/s")
col2.metric("Rotacional en la pared", f"(0, {rotacional_max:.1f}, 0) s⁻¹")
col3.metric("Circulación Eje Central (C1)", f"{circulacion_central:.2f} m²/s")

st.subheader("Representaciones del Campo Vectorial")
col_fig1, col_fig2 = st.columns(2)

with col_fig1:
    r_grid = np.linspace(0, R, 30)
    theta_grid = np.linspace(0, 2*np.pi, 40)
    r_mesh, theta_mesh = np.meshgrid(r_grid, theta_grid)
    X2 = r_mesh * np.cos(theta_mesh)
    Y2 = r_mesh * np.sin(theta_mesh)
    V_z2 = v_max * (1 - (X2**2 + Y2**2) / R**2)

    fig2d, ax2d = plt.subplots(figsize=(5, 5))
    c = ax2d.contourf(X2, Y2, V_z2, levels=50, cmap='viridis')
    fig2d.colorbar(c, label='Velocidad $v_z$ (m/s)')
    círculo = plt.Circle((0, 0), R, color='black', fill=False, linewidth=2, linestyle='--')
    ax2d.add_patch(círculo)
    ax2d.set_title('Corte Transversal 2D')
    ax2d.set_xlabel('X (m)')
    ax2d.set_ylabel('Y (m)')
    ax2d.set_aspect('equal')
    st.pyplot(fig2d)

with col_fig2:
    X_vals, Y_vals = [], []
    for r_i in np.linspace(0, R, 6):
        if r_i == 0:
            X_vals.append(0)
            Y_vals.append(0)
        else:
            num_pts = int(24 * (r_i / R))
            theta_i = np.linspace(0, 2*np.pi, num_pts, endpoint=False)
            X_vals.extend(r_i * np.cos(theta_i))
            Y_vals.extend(r_i * np.sin(theta_i))

    X3_v = np.array(X_vals)
    Y3_v = np.array(Y_vals)
    W = v_max * (1 - (X3_v**2 + Y3_v**2) / R**2)

    fig3d = plt.figure(figsize=(6, 5))
    ax3d = fig3d.add_subplot(111, projection='3d')
    
    # Truco de flechas manuales para Streamlit
    for x, y, w in zip(X3_v, Y3_v, W):
        ax3d.plot([x, x], [y, y], [0, w], color='blue', linewidth=1.2, alpha=0.7)
    ax3d.scatter(X3_v, Y3_v, W, color='blue', marker='^', s=35, alpha=0.9, depthshade=False)
    
    theta_c = np.linspace(0, 2*np.pi, 100)
    ax3d.plot(R*np.cos(theta_c), R*np.sin(theta_c), 0, color='black', linewidth=2, linestyle='--')
    
    ax3d.set_title('Campo Vectorial 3D')
    ax3d.set_xlabel('X (m)')
    ax3d.set_ylabel('Y (m)')
    ax3d.set_zlabel('v_z (m/s)')
    ax3d.set_zlim(0, max(1.0, v_max * 1.1))
    st.pyplot(fig3d)
