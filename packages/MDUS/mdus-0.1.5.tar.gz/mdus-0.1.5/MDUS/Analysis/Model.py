import KT17

def CalcModel(self, model="KT17",
              Rsun=0.4, DI=50):
    coordinates = ['X_MSO','Y_MSO','Z_MSO']
    columns = self.value.columns
    if not set(coordinates).issubset(columns):
        raise ValueError("Data does not contain required coordinates. "\
        "you need to use GetPos()")
    # DI limits
    if DI < 0:
        print("DI should be non-negative. Setting DI=0")
        DI = 0
    if DI > 97:
        print("DI is too large. Setting DI=97")
        DI = 97
    # Model
    if model == "KT17":
        x_model, y_model, z_model = KT17.ModelField(
            self.value["X_MSO"].values,
            self.value["Y_MSO"].values,
            self.value["Z_MSO"].values,
            Rsun=Rsun, DistIndex=DI
        )
    self.value['Bx_model'] = x_model
    self.value['By_model'] = y_model
    self.value['Bz_model'] = z_model