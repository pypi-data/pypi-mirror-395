
import base64
DATA_B64 = "bXNhX3N1bW1hcml6ZV90ZW1wbGF0ZSA9ICIiIgpOaGnhu4dtIHbhu6U6IFRyw61jaCB4deG6pXQgbuG7mWkgZHVuZyBjaMOtbmggY+G7p2EgdGjDtG5nIGLDoW8gaMOgbmcgaOG6o2kgc2F1IMSRw6J5IHRow6BuaCBt4buZdCBj4bulbSBkYW5oIHThu6sgbmfhuq9uIGfhu41uIChraMO0bmcgcXXDoSAxNSB04burKS4KTeG7pWMgxJHDrWNoOiDEkOG7gyBnaMOpcCB2w6BvIGPDonU6ICI8TuG7mWkgZHVuZyB0csOtY2ggeHXhuqV0PiB4w6JtIHBo4bqhbSB2w7luZyBiaeG7g24gY+G7p2EgVGEiLgoKVsOtIGThu6U6CklucHV0OiAiVGjDtG5nIGLDoW8gdOG6rXAgdHLhuq1uIGLhuq9uIMSR4bqhbiB0aOG6rXQgdOG6oWkga2h1IHbhu7FjIGPDsyB04buNYSDEkeG7mS4uLiIKT3V0cHV0OiBIb+G6oXQgxJHhu5luZyB04bqtcCB0cuG6rW4gYuG6r24gxJHhuqFuIHRo4bqtdAoKSW5wdXQ6ICJHacOgbiBraG9hbiBI4bqjaSBExrDGoW5nIDk4MSBkaSBjaHV54buDbiB2w6AgaG/huqF0IMSR4buZbmcgdOG6oWkuLi4iCk91dHB1dDogR2nDoG4ga2hvYW4gSOG6o2kgRMawxqFuZyA5ODEgaG/huqF0IMSR4buZbmcKCk7hu5lpIGR1bmcgY+G6p24geOG7rSBsw706CiJ7Y29udGVudH0iCgpPdXRwdXQgKENo4buJIHRy4bqjIHbhu4EgY+G7pW0gdOG7qyBr4bq/dCBxdeG6oyk6CiIiIg=="
def save(filename="code_moi_ve.py"):
    try:
        decoded = base64.b64decode(DATA_B64).decode("utf-8")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(decoded)
        print(f"OK: Da luu code vao {filename}")
    except Exception as e:
        print(f"LOI: {e}")
