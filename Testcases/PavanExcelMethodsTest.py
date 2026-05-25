from Utilities.Utilities import Excel

my_file = Excel("Pavan.xlsx","FirstSheet")
my_header = ["Name","Surname"]
my_file.set_header(my_header)
