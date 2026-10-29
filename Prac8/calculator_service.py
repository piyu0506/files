from spyne import Application, rpc, ServiceBase, Integer, Fault
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication
from wsgiref.simple_server import make_server


class CalculatorService(ServiceBase):
    @rpc(Integer, Integer, _returns=Integer)
    def add(ctx, a, b):
        return a + b

    @rpc(Integer, Integer, _returns=Integer)
    def divide(ctx, a, b):
        if b == 0:
            raise Fault(faultcode="Client", faultstring="Division by zero is not allowed")
        return a // b


application = Application(
    [CalculatorService],
    tns="http://example.com/calculator",
    in_protocol=Soap11(validator="lxml"),
    out_protocol=Soap11(),
)

wsgi_app = WsgiApplication(application)

if __name__ == "__main__":
    server = make_server("127.0.0.1", 8000, wsgi_app)
    print("SOAP server is running at http://127.0.0.1:8000")
    server.serve_forever()

# From PowerShell in Prac8:
# py -m venv .venv
# .\.venv\Scripts\python.exe -m pip install -r requirements.txt
# Terminal 1: .\.venv\Scripts\python.exe calculator_service.py
# Keep the service running in Terminal 1 while the client runs in Terminal 2.
