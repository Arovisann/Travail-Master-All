import h5py

file_path = r"C:\Users\alexa\Documents\OpenSignals (r)evolution\temp\opensignals_201806130253_2025-04-15_10-57-37.h5"


def explore_h5_file(file_path):
    def print_attrs(name, obj):
        print(f"\n📁 {name}")
        for key, val in obj.attrs.items():
            print(f"   ⤷ Attribute - {key}: {val}")
        if isinstance(obj, h5py.Dataset):
            print(f"   ⤷ Dataset shape: {obj.shape}, dtype: {obj.dtype}")
            try:
                preview = obj[()]
                if isinstance(preview, (list, tuple)) or preview.ndim > 1:
                    print("   ⤷ Preview (first 5 elements):", preview[:5])
                else:
                    print("   ⤷ Value:", preview)
            except Exception as e:
                print(f"   ⤷ Could not read dataset preview: {e}")

    with h5py.File(file_path, 'r') as h5file:
        print(f"\n📂 Exploring HDF5 file: {file_path}")
        h5file.visititems(print_attrs)

# Exemple d'utilisation
explore_h5_file(r"C:\Users\alexa\Documents\OpenSignals (r)evolution\temp\opensignals_201806130253_2025-04-15_10-57-37.h5")

