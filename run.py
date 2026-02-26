import tkinter as tk
from ui import BarPOSUI

# replicate original menu data (abbreviated for compactness)
MENU_DATA = [
    ["PANEER TIKKA", "1", 240.00],
    ["PANEER BUTTER MASALA", "1", 280.00],
    ["VEG CRISPY", "1", 180.00],
    ["DAL TADKA", "1", 150.00],
    ["CHICKEN LOLLIPOP", "6PC", 220.00],
    ["ROYAL STAG", "NIP", 290.00],
    ["BLENDERS PRIDE", "NIP", 380.00],
    ["COKE 500ML", "1", 60.00],
    ["MINERAL WATER", "1L", 30.00],
    ["CHICKEN CHILLI", "1", 210.00],
]

def main():
    root = tk.Tk()
    app = BarPOSUI(root, MENU_DATA)
    root.mainloop()

if __name__ == '__main__':
    main()
