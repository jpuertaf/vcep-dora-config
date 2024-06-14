import os

# Define the package name to search for
package_name = "Microsoft.Azure.DocumentDB.Core"

# Define the root directory of the solution
root_dir = r"C:\Users\jpuerta\source\repos\volvo-cars\vcep-int-inbound-contact"

# Function to search for package reference in specified files
def search_package_references(root_dir, package_name):
    results = []
    # Walk through the directory
    for subdir, _, files in os.walk(root_dir):
        for file in files:
            if file.endswith((".csproj", "packages.config", "Directory.Build.props", "Directory.Build.targets")):
                file_path = os.path.join(subdir, file)
                found = False
                with open(file_path, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    for line in lines:
                        if package_name in line:
                            results.append((file_path, line.strip()))
                            found = True
                            break
                if not found:
                    results.append((file_path, None))
    return results

# Search for the package references
results = search_package_references(root_dir, package_name)

# Output the results
for result in results:
    if result[1]:
        print(f"Project/File: {result[0]}")
        print(f"Package Reference Found: {result[1]}")
    else:
        print(f"Project/File: {result[0]}")
        print("Package Reference Not Found")
    print()
