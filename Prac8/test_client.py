from zeep import Client
from zeep.exceptions import Fault


def main() -> None:
    wsdl_url = "http://127.0.0.1:8000/?wsdl"
    client = Client(wsdl=wsdl_url)

    print("10 + 5 =", client.service.add(10, 5))
    print("20 / 4 =", client.service.divide(20, 4))

    try:
        print("20 / 0 =", client.service.divide(20, 0))
    except Fault as e:
        print("SOAP Fault:", e)


if __name__ == "__main__":
    main()

# From PowerShell in Prac8, open a second terminal:
# .\.venv\Scripts\python.exe test_client.py
# The service must remain running in the first terminal while this client executes.
