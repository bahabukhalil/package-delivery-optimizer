import streamlit as st
import matplotlib.pyplot as plt
from models import Parcel, Van, generate_random_data, load_user_input_file
from genetic_algorithm import GeneticAlgorithmSolver
from simulated_annealing import SimulatedAnnealingSolver
from PIL import Image
import io
import pandas as pd
import numpy as np

st.set_page_config(page_title="AI Delivery Optimizer", layout="wide")
COLORS = ['red', 'blue', 'green', 'orange', 'purple', 'cyan', 'magenta', 'brown', 'pink', 'olive']


def visualize_solution(solution):
    plt.figure(figsize=(10, 8))
    plt.scatter(0, 0, s=200, c='black', marker='*', label='Shop')
    for idx, van in enumerate(solution.vans):
        color = COLORS[idx % len(COLORS)]
        if not van.assigned_parcels:
            continue
        x_coords = [0] + [p.x for p in van.assigned_parcels] + [0]
        y_coords = [0] + [p.y for p in van.assigned_parcels] + [0]
        plt.plot(x_coords, y_coords, 'o-', color=color, linewidth=2,
                 label=f'Van {van.id} ({len(van.assigned_parcels)} parcels)')
        for p in van.assigned_parcels:
            plt.annotate(f"P{p.id}\\n(Pri:{p.priority})", (p.x, p.y), textcoords="offset points", xytext=(0, 5))
    plt.title("Package Delivery Routes")
    plt.xlabel("X Coordinate (km)")
    plt.ylabel("Y Coordinate (km)")
    plt.grid(True)
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf


def convert_df_to_parcels(df):
    parcels = []
    for i, row in df.iterrows():
        parcels.append(Parcel(int(row["ID"]), float(row["X"]), float(row["Y"]), float(row["Weight"]), int(row["Priority"])))
    return parcels


def main():
    with st.sidebar:
        st.title("Delivery Optimizer")
        try:
            logo = Image.open("baha_shadi.jpg")
            st.image(logo, caption="Powered by BAHA and SHADI", width=250)
        except:
            st.warning("Logo not found.")
        st.info("ENCS3340 Project #1")

    st.title("Package Delivery Route Optimization")

    input_method = st.radio("Choose Input Method", ["Generate Random", "Upload Text File"], horizontal=True)

    vans, parcels = [], []

    if input_method == "Generate Random":
        col1, col2 = st.columns(2)
        num_vans = col1.slider("Number of vans", 1, 10, 3)
        num_parcels = col2.slider("Number of parcels", 1, 50, 10)
        if st.button("Generate Data"):
            vans, parcels = generate_random_data(num_vans, num_parcels)
            st.session_state.vans = vans
            st.session_state.parcels = parcels
            st.success("Random data generated.")

    elif input_method == "Upload Text File":
        uploaded_file = st.file_uploader("Upload `.txt` input file", type="txt")
        if uploaded_file:
            try:
                content = uploaded_file.read().decode("utf-8").splitlines()
                vans, parcels = load_user_input_file(
                    [l.strip() for l in content if l.strip() and not l.startswith("#")])
                st.session_state.vans = vans
                st.session_state.parcels = parcels
                st.success("File loaded successfully.")
            except Exception as e:
                st.error(f"Error parsing file: {e}")

    if "vans" in st.session_state and "parcels" in st.session_state:
        st.markdown("### Current Parcel Data")
        df = pd.DataFrame([{"ID": p.id, "X": round(p.x, 2), "Y": round(p.y, 2),
                            "Weight": round(p.weight, 2), "Priority": p.priority}
                           for p in st.session_state.parcels])
        st.dataframe(df)

    st.markdown("---")
    st.subheader("Choose Algorithm")
    algorithm = st.radio("Optimization Algorithm", ["Genetic Algorithm", "Simulated Annealing"], horizontal=True)

    if algorithm == "Genetic Algorithm":
        population_size = st.slider("Population Size", 50, 100, 75)
        mutation_rate = st.slider("Mutation Rate", 0.01, 0.1, 0.05, step=0.01)
    else:
        cooling_rate = st.slider("Cooling Rate", 0.90, 0.99, 0.95, step=0.01)

    if st.button("Run Optimization", type="primary"):
        if "vans" not in st.session_state or "parcels" not in st.session_state:
            st.error("Missing data. Please provide input.")
        else:
            vans = st.session_state.vans
            parcels = st.session_state.parcels
            with st.spinner("Running optimization..."):
                try:
                    if algorithm == "Genetic Algorithm":
                        solver = GeneticAlgorithmSolver(vans, parcels, population_size, mutation_rate, 500)
                    else:
                        solver = SimulatedAnnealingSolver(vans, parcels, 1000, cooling_rate, 1, 100)

                    solution = solver.solve()
                    st.success("Optimization complete.")

                    total_distance = solution.calculate_total_distance()
                    total_parcels = sum(len(v.assigned_parcels) for v in solution.vans)

                    col1, col2, col3 = st.columns(3)
                    col1.metric("Total Distance", f"{total_distance:.2f} km")
                    col2.metric("Total Parcels", total_parcels)
                    col3.metric("Total Vans", len(solution.vans))

                    st.markdown("### Detailed Results")
                    for v in solution.vans:
                        with st.expander(f"Van {v.id}"):
                            st.write(f"Capacity: {v.capacity:.2f} kg")
                            st.write(f"Used: {v.capacity - v.remaining_capacity():.2f} kg")
                            st.write(f"Distance: {v.calculate_route_distance():.2f} km")
                            st.table([{"ID": p.id, "Location": f"({p.x:.1f},{p.y:.1f})", "Weight": p.weight, "Priority": p.priority}
                                      for p in v.assigned_parcels])

                    st.image(visualize_solution(solution), caption="Optimized Delivery Routes", use_container_width=True)

                    if st.download_button("Download CSV", df.to_csv(index=False), file_name="optimized_parcels.csv"):
                        st.success("CSV downloaded.")

                except Exception as e:
                    st.error(f"Execution error: {e}")


if __name__ == "__main__":
    main()