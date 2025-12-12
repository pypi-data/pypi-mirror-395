import os
import subprocess
import time
import shutil
import tempfile
import urllib.request
from n8nControl.response import appResponse
from fastapi import HTTPException
import sqlite3, json, time, os
import uuid
import requests
import socket

class N8nManagement:
    container_name = "n8n"
    db_path = "/root/n8n/database.sqlite"
    def __init__(self,):
        print("N8nManagement initialized")

    
    def import_workflow(self, file_remote):
        try:
            filename = os.path.basename(file_remote)
            container_upload_dir = "/home/node/.n8n/uploads"
            container_file_path = f"{container_upload_dir}/{filename}"
            # use a temporary path inside the container (not the uploads bind mount)
            container_tmp_path = f"/tmp/{filename}"
            # check folder exsits 
            check_dir_cmd = [
                "docker", "exec", self.container_name,
                "sh", "-c",
                f"if [ ! -d '{container_upload_dir}' ]; then mkdir -p '{container_upload_dir}' && chmod -R 777 '{container_upload_dir}'; fi"
            ]
            subprocess.run(check_dir_cmd, check=True)
        
            copy_cmd = ["docker", "cp", file_remote, f"{self.container_name}:{container_tmp_path}"]
            subprocess.run(copy_cmd, check=True)

            subprocess.run([
                "docker", "exec", self.container_name,
                "sh", "-c",
                f"chmod 644 '{container_tmp_path}'"
            ], check=False)

            subprocess.run([
                "docker", "exec", "--user", "root", self.container_name,
                "sh", "-c",
                f"chown node:node '{container_tmp_path}'"
            ], check=False)
            

            cmd = [
                "docker", "exec", self.container_name,
                "n8n", "import:workflow",
                f"--input={container_tmp_path}",
                "--overwrite"
            ]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("import_workflow stdout:", result.stdout)
                print("import_workflow stderr:", result.stderr)
                raise HTTPException(status_code=500, detail=f"n8n import failed: {(result.stderr or '').strip()}")

            return appResponse.AppResponse("success", "Import workflow success", None)
        except Exception as e:
            print(f"❌ import_workflow failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))


    def export_workflow(self):
        try:
            timestamp = int(time.time())
            container_tmp_path = f"/tmp/workflows-export-{timestamp}.json"

        
            export_cmd = [
                "docker", "exec", self.container_name,
                "n8n", "export:workflow",
                "--all",
                f"--output={container_tmp_path}"
            ]

            result = subprocess.run(export_cmd, capture_output=True, text=True)
            if result.returncode != 0:
                print("export_workflow stdout:", result.stdout)
                print("export_workflow stderr:", result.stderr)
                raise HTTPException(status_code=500, detail=f"n8n export failed: {(result.stderr or '').strip()}")

        
            export_dir = "/root/n8n_exports"
            os.makedirs(export_dir, exist_ok=True)

            host_file_path = os.path.join(export_dir, f"workflows-export-{timestamp}.json")

        
            copy_out_cmd = [
                "docker", "cp",
                f"{self.container_name}:{container_tmp_path}",
                host_file_path
            ]
            subprocess.run(copy_out_cmd, check=True)

            return {
                "filePath": host_file_path,
                "filename": f"workflows-export-{timestamp}.json"
            }

        except Exception as e:
            print(f"❌ export_workflow failed: {e}")
            raise HTTPException(status_code=500, detail="n8n export failed")



    def change_domain(self,new_domain):
        nginx_conf = f"""
server {{
    listen 80;
    server_name _;

    return 444;
}}

server {{
    listen 80;
    server_name {new_domain};

    location / {{
        proxy_pass http://127.0.0.1:5678;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }}
}}
""".strip()

        remote_path = "/etc/nginx/conf.d/n8n.conf"

        try:
            with open(remote_path, "w") as f:
                f.write(nginx_conf)

            subprocess.run(["nginx", "-t"], check=True)
            subprocess.run(["systemctl", "reload", "nginx"], check=True)

            return appResponse.AppResponse("success", "Domain changed successfully", None)

        except Exception as e:
            print(f"❌ changeDomain failed: {e}")

    def reset_user_info(self):
        try:
            result = subprocess.run(
                ["docker", "exec", "-i", self.container_name, "n8n", "user-management:reset"],
                capture_output=True,
                text=True,
                check=True
            )

            print("stdout:", result.stdout)
            print("stderr:", result.stderr)
            subprocess.run(["docker", "restart", self.container_name], check=True)

            return appResponse.AppResponse("success", "Reset user info successfully", None)
        except Exception as e:
            print(f"❌ n8n export failed: {e}")
            raise HTTPException(status_code=500, detail="reset failed")

    def update_version(self,version):
        try:
            print(f"🆙 Updating n8n to version {version}")
            subprocess.run(["docker", "pull", f"n8nio/n8n:{version}"], check=True)

            subprocess.run(["docker", "stop", self.container_name], check=True)

            subprocess.run([
            "docker", "run", "-d",
            "--name", f"{self.container_name}_new",
            "--restart=always",
            "-p", "5678:5678",
            "-v", "/root/n8n:/home/node/.n8n",
            f"n8nio/n8n:{version}"
            ], check=True)
            subprocess.run(["docker", "rm", self.container_name], check=False)

            subprocess.run(["docker", "rename", f"{self.container_name}_new", self.container_name], check=True)

            return appResponse.AppResponse("success", f"Updated n8n to version {version}", None)
        except Exception as e:
            print(f"❌ update_version failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    def get_version_n8n(self):
        try:
            result = subprocess.run([
                "docker", "exec", self.container_name, "n8n", "--version"
            ], capture_output=True, text=True, check=True)
            version = (result.stdout or "").strip()
            return appResponse.AppResponse("success", f"n8n version is {version}", {
                "version": version
            })
        except Exception as e:
            print(f"❌ get_version_n8n failed: {e}")
            raise HTTPException(status_code=500, detail=str(e))
    def set_domain_init(self):
        response = requests.post("https://lev-api.n8njoy.com/api2/public/get-n8n-domain")
        struct =response.json()
        print(struct)
        print(struct["data"]["ip"])
        if struct["status"] == 'error':
            raise Exception("error to get domain")
        content = struct["data"]["n8n_domain"]
        domain = content.replace("https://", "").replace("http://", "")
        nginx_conf = f"""
server {{
    listen 80;
    server_name _;

    return 444;
}}

server {{
    listen 80;
    server_name {domain};

    location / {{
        proxy_pass http://127.0.0.1:5678;
        proxy_http_version 1.1;

        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }}
}}
""".strip()
        nginx_conf_agent =f"""
server {{
    listen 80;
        server_name {struct["data"]["ip"]};
        location / {{
            proxy_pass http://127.0.0.1:9000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
            proxy_read_timeout 300;
            proxy_connect_timeout 300;
            proxy_send_timeout 300;
        }}
}}
""".strip()

        remote_path = "/etc/nginx/conf.d/n8n.conf"
        remote_path_agent ="/etc/nginx/conf.d/n8napp.conf"
        try:
            with open(remote_path, "w") as f:
                f.write(nginx_conf)
            with open(remote_path_agent,"w") as f:
                f.write(nginx_conf_agent)
            subprocess.run(["nginx", "-t"], check=True)
            subprocess.run(["systemctl", "reload", "nginx"], check=True)
            ip=struct["data"]["ip"]
            domain_dns = domain.split('.')[0]
            key="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJzZXJ2ZXIiOiJkbnMifQ.jLyRb-teMcwclrGoOVLFq0xr2UosQE84DFSM_pqUD3s"
            endPoint = f"http://148.163.73.102/add_record?subdomain={domain_dns}&record_type=A&value={ip}"
            headers = {
                "Authorization": f"Bearer {key}"
            }

            result = requests.post(endPoint, headers=headers)
            print(result)
            return appResponse.AppResponse("success", "Domain changed successfully", None)

        except Exception as e:
            print(f" Set domain failed: {e}")
            
