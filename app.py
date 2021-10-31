import typing
from pprint import pprint
from flask import Flask, jsonify, request
from escpos.printer import Win32Raw
from utils import leftright

app = Flask(__name__)


@app.route("/", methods=["POST"], defaults={"path": ""})
@app.route("/<path:path>", methods=["POST"])
def hello_world(path):
    p = Win32Raw()
    p.set(font='a')
    j = request.get_json()
    p.set(align='center')
    p.image('celfun.png', high_density_vertical=True, high_density_horizontal=True)
    p.set(align='center', bold=False, double_height=False, double_width=False)
    p.text("\nHEZC850515PY1\n")
    p.text("Col. Cuernavaca Centro c.p. 62000\n")
    p.text("Cuernavaca, Morelos\n")
    p.text("******************************************\n\n")
    for product in j:
        leftright(p, left=product["desc"], right=product["price"], font='a')

    p.text("\n******************************************\n\n")
    p.barcode('{B7503028490974', 'CODE128', function_type="B", width=2)
    p.qr("https://celfun.com", size=8)
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
