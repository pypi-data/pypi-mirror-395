import uvicorn

def main():
    # run the app via the package module path so uvicorn can import it when installed
    uvicorn.run(app="sohyloha.main:app", host="0.0.0.0", port=8000)

if __name__ == "__main__":
    main()
