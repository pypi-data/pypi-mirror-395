import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression
from pygam import LinearGAM, s

# Generate synthetic temperature data (in degrees Celsius)
np.random.seed(42)
n = 200
temperature = np.random.uniform(
    -10, 45, n
)  # Wider temperature range from -10°C to 45°C

# Simulate a non-linear relationship between temperature and yield (in tons/ha)
# Yield approaches 0 at very low and very high temperatures, peaks at moderate temperatures (~25°C)
yield_true = -0.05 * (temperature - 25) ** 2 + 5 + np.random.normal(0, 0.5, n)
yield_true = np.clip(yield_true, 0, None)  # Ensure yield is non-negative

# Reshape temperature for sklearn models
X = temperature.reshape(-1, 1)

# Fit Linear Regression model
linear_model = LinearRegression().fit(X, yield_true)

# Fit Polynomial Regression model (degree=2)
poly2 = PolynomialFeatures(degree=2)
X_poly2 = poly2.fit_transform(X)
poly_model2 = LinearRegression().fit(X_poly2, yield_true)

# Fit Polynomial Regression model (degree=3)
poly3 = PolynomialFeatures(degree=3)
X_poly3 = poly3.fit_transform(X)
poly_model3 = LinearRegression().fit(X_poly3, yield_true)

# Fit Polynomial Regression model (degree=4)
poly4 = PolynomialFeatures(degree=4)
X_poly4 = poly4.fit_transform(X)
poly_model4 = LinearRegression().fit(X_poly4, yield_true)

# Fit GAM model with a smooth term for temperature
gam = LinearGAM(s(0)).fit(X, yield_true)

# Create predictions over a range of temperatures for plotting
temp_range = np.linspace(-10, 45, 500).reshape(
    -1, 1
)  # 500 points between -10°C and 45°C
yield_pred_linear = linear_model.predict(temp_range)
yield_pred_poly2 = poly_model2.predict(poly2.transform(temp_range))
yield_pred_poly3 = poly_model3.predict(poly3.transform(temp_range))
yield_pred_poly4 = poly_model4.predict(poly4.transform(temp_range))
yield_pred_gam = gam.predict(temp_range)

with plt.style.context("science"):
    # Plot the results
    plt.figure(figsize=(10, 6))

    # Scatter plot of the true data
    plt.scatter(temperature, yield_true, color="blue", alpha=0.6, label="True Data")

    # Plot predictions from Linear Regression
    plt.plot(
        temp_range,
        yield_pred_linear,
        color="green",
        linestyle="--",
        label="Linear Model",
        linewidth=1.5,
    )

    # Plot predictions from Polynomial Regression (degree=2)
    plt.plot(
        temp_range,
        yield_pred_poly2,
        color="orange",
        linestyle="-.",
        label="Polynomial Model (Degree 2)",
        alpha=0.5,
        linewidth=1.5,
    )

    # Plot predictions from Polynomial Regression (degree=3)
    plt.plot(
        temp_range,
        yield_pred_poly3,
        color="purple",
        linestyle="-.",
        label="Polynomial Model (Degree 3)",
        alpha=0.5,
        linewidth=1.5,
    )

    # Plot predictions from Polynomial Regression (degree=4)
    plt.plot(
        temp_range,
        yield_pred_poly4,
        color="brown",
        linestyle="-.",
        label="Polynomial Model (Degree 4)",
        alpha=0.5,
        linewidth=1.5,
    )

    # Plot predictions from GAM
    plt.plot(temp_range, yield_pred_gam, color="red", label="GAM Model", linewidth=1.5)

    # Labels and title
    plt.xlabel("Temperature (°C)", fontsize=16)
    plt.ylabel("Crop Yield (Mg/ha)", fontsize=16)
    # plt.title('Comparison of Linear, Polynomial (Degrees 2-4), and GAM Models for Yield vs Temperature')
    plt.legend()

    # Show the plot
    plt.tight_layout()
    plt.show()

    # Plot the partial dependence for the temperature feature (s(0))
    XX = gam.generate_X_grid(term=0)
    pdep = gam.partial_dependence(term=0, X=XX)

    plt.plot(XX[:, 0], pdep, color="red", label="GAM Partial Dependence")
    plt.tick_params(axis="both", which="major", labelsize=12)
    plt.xlabel("Temperature (°C)")
    plt.ylabel("Partial Effect on Yield")
    plt.title("GAM Partial Dependence: Temperature")
    plt.legend()
    plt.show()
