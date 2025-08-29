import subprocess

if __name__ == '__main__':
    subprocess.Popen(["poetry", "run", "python", "Agents/agent.py"])
    subprocess.run(["poetry", "run", "python", "Server/rest.py"])