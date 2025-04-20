import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

mu, sigma = 0, 1
x = np.linspace(mu - 4 * sigma, mu + 4 * sigma, 1000)
y = norm.pdf(x, mu, sigma)

plt.figure(figsize=(8, 5))
plt.plot(x, y)
plt.title("Normal Distribution")
plt.savefig("test.jpg", format="jpg")
plt.close()
print("圖檔已儲存為 test.jpg")