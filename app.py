import typing
from pprint import pprint
from flask import Flask, jsonify, request
from escpos.printer import Win32Raw,Usb
from utils import leftright
from sys import platform as _platform


app = Flask(__name__)
type = 'reparacion'


@app.route("/", methods=["POST"], defaults={"path": ""})
@app.route("/<path:path>", methods=["POST"])
def hello_world(path):
    if _platform == "win64" or _platform == "win32":
        p = Win32Raw()
    else:
        p = Usb(0x04b8, 0xa700)
    p.set(font='a')
    j = request.get_json()
    p.set(align='center')
    p.image('celfun.png', high_density_vertical=True, high_density_horizontal=True)
    p.set(align='center', bold=False, double_height=False, double_width=False)
    p.text("\nHEZC850515PY1\n")
    p.text("Col. Cuernavaca Centro c.p. 62000\n")
    p.text("Cuernavaca, Morelos\n")

    p.set(align='center', bold=True, double_height=True, double_width=True)
    p.text("ORDEN DE SERVICIO\n")
    p.set(align='center', bold=False, double_height=False, double_width=False)
    p.text("******************************************\n\n")
    if type == 'venta':
        for product in j:
            leftright(p, left=product["desc"], right=product["price"], font='a')
    if type == 'reparacion':
        leftright(p, left="Cliente", right="Alejandro Hernandez", font='a')
        leftright(p, left="Equipo:", right="Apple iPhone 7 negro", font='a')
        leftright(p, left="Imei:", right="355316082611279", font='a')
        leftright(p, left="Falla:", right="Display roto", font='a')
        leftright(p, left="Notas:", right="", font='a')
        p.text("No se pudo verificar funcionamiento del equipo.\n")
        leftright(p, left="Presupuesto:", right="$950.00", font='a')

    p.text("\n******************************************\n\n")
    p.barcode('{B00000089', 'CODE128', function_type="B", width=2)
    p.set(align='center', font='b')
    p.text("Verifique si su equipo ya esta reparado escaneando el siguiente codigo:")
    p.qr("https://celfun.com", size=8)
    p.text("Consulte garantia y aviso de privacidad en celfun.com")
    p.cut()
    p.close()

    print(f"*** Received data at: {path}")
    print("\n** json:")
    pprint(j)

    return jsonify(
        {
            "endpoint": path,
            "data": request.data.decode("utf-8"),
            "form": request.form,
            "json": request.get_json(),
        }
    )


if __name__ == '__main__':
    app.run()
