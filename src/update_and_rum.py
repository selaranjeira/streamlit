import subprocess
import os

def run_script(script_name):
    print(f"Running script: {script_name}")
    subprocess.run(["python3", script_name], check=True)

def main():
    # Atualizar o banco de dados
    run_script("/home/selaranjeira/Desktop/loc_proj/desemp_esportivo/src/data_processing/upload.py")

    # Rodar o aplicativo Streamlit
    script_path = os.path.join("src", "app.py")
    print(f"Running Streamlit app: {script_path}")
    subprocess.run(["streamlit", "run", script_path], check=True)

if __name__ == "__main__":
    main()
