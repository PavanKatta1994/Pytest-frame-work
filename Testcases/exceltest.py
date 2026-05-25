from Utilities.Utilities import Excel

myfile = Excel("test.xlsx","MyData")
# myfile.add_header(["Name","Surname"])
# myfile.add_data(["Pavan","Katta"])
# myfile.add_data(["Lavanya","Katta"])
# myfile.add_data(["Prasad","Bandaru"])
# myfile.add_data(["Sathish","Chinthalpudi"])
# myfile.save_excel()

value = myfile.read_column_data({"Surname":"Katta"},"Name")
print(value)
value = myfile.modify_column_data({"Surname":"Katta","Name":"Prasad"},"Surname","Bandaru")
myfile.save_excel()