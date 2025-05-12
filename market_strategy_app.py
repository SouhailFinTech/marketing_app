import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# --------------------------
# 1. Define simulation parameters
# --------------------------

def simulate_strategy(
    price,
    cost,
    elasticity,
    market_size,
    strategy_type,
    simulations=10000,
    noise_std=0.05
):
    np.random.seed(42)
    
    # Simulate demand using price elasticity model
    base_demand = market_size * (1 - elasticity * (price - cost) / cost)
    
    # Add noise to simulate uncertainty
    demand_dist = np.random.normal(loc=base_demand, scale=base_demand * noise_std, size=simulations)
    demand_dist = np.clip(demand_dist, 0, market_size)  # no negative or more than market
    
    # Revenue and profit
    revenue = demand_dist * price
    profit = demand_dist * (price - cost)

    results = pd.DataFrame({
        "Demand": demand_dist,
        "Revenue": revenue,
        "Profit": profit
    })
    
    return results


# --------------------------
# 2. Streamlit App Interface
# --------------------------

def main():
    st.title("📈 Market Entry Strategy Simulator")
    st.markdown("""
        Simulate different pricing strategies to estimate potential revenue and profit
        before launching your product in a competitive market.
    """)

    with st.sidebar:
        st.header("Strategy Parameters")
        strategy = st.selectbox("Select Strategy", ["Low Price", "Premium", "Penetration", "Custom"])

        if strategy == "Low Price":
            price = 3
        elif strategy == "Premium":
            price = 10
        elif strategy == "Penetration":
            price = 1.5
        else:
            price = st.slider("Set Your Product Price", 1.0, 20.0, 5.0)

        cost = st.number_input("Production Cost per Unit ($)", value=2.0, min_value=0.1)
        elasticity = st.slider("Price Elasticity (0.1 = inelastic, >1 = very sensitive)", 0.1, 2.0, 1.0)
        market_size = st.number_input("Target Market Size (people)", value=10000)

    # Run simulation
    results = simulate_strategy(price, cost, elasticity, market_size, strategy)

    # KPIs
    st.subheader("📊 Simulation Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Avg Revenue ($)", f"{results['Revenue'].mean():,.2f}")
    col2.metric("Avg Profit ($)", f"{results['Profit'].mean():,.2f}")
    col3.metric("Break-even Chance", f"{(results['Profit'] > 0).mean() * 100:.2f}%")

    # Charts
    st.subheader("📉 Profit Distribution")
    fig, ax = plt.subplots()
    ax.hist(results['Profit'], bins=50, color='skyblue', edgecolor='black')
    ax.set_xlabel("Profit ($)")
    ax.set_ylabel("Frequency")
    st.pyplot(fig)

    st.subheader("📈 Revenue vs Demand (sample)")
    st.scatter_chart(results.sample(1000)[['Demand', 'Revenue']])

    # Show raw data
    with st.expander("🔍 View Raw Simulation Data"):
        st.dataframe(results.head(100))


if __name__ == "__main__":
    main()