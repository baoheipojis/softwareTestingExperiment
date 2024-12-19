import pandas as pd
import matplotlib.pyplot as plt

# Read CSV file
df = pd.read_csv('onelist_perf.csv')

# Confirm data columns
print(df.columns)

# Plot total Pss over test runs
plt.figure(figsize=(10, 6))
plt.plot(df['totalPss'], marker='o', linestyle='-', label='Total Pss')
plt.xlabel('Test Runs')
plt.ylabel('Total Pss')
plt.title('Total Pss over Test Runs')
plt.legend()
plt.grid(True)
plt.savefig('totalPss_over_tests.png')
plt.show()

# Plot comparison of Native Pss and Dalvik Pss
plt.figure(figsize=(10, 6))
plt.plot(df['nativePss'], marker='x', linestyle='-', label='Native Pss')
plt.plot(df['dalvikPss'], marker='s', linestyle='--', label='Dalvik Pss')
plt.xlabel('Test Runs')
plt.ylabel('Pss Value')
plt.title('Comparison of Native Pss and Dalvik Pss')
plt.legend()
plt.grid(True)
plt.savefig('native_vs_dalvikPss.png')
plt.show()

# Plot Native Heap Size
plt.figure(figsize=(10, 6))
plt.plot(df['nativeHeapSize'], marker='^', linestyle='-', color='green', label='Native Heap Size')
plt.xlabel('Test Runs')
plt.ylabel('Native Heap Size')
plt.title('Native Heap Size over Test Runs')
plt.legend()
plt.grid(True)
plt.savefig('nativeHeapSize_over_tests.png')
plt.show()