#!/bin/bash
echo "Executa a aplicação backend principal"
uvicorn main:app_media --reload