from flask import jsonify, request
from backend.services.chamado_service import ChamadoService

class ChamadoController:
    @staticmethod
    def criar_chamado():
        data = request.json
        titulo = data.get("titulo")
        descricao = data.get("descricao")
        
        if not all([titulo, descricao]):
            return jsonify({"erro": "Todos os campos são obrigatórios"}), 400

        chamado_id = ChamadoService.criar_chamado(titulo, descricao, request.userid)
        return jsonify({"mensagem": "Chamado criado com sucesso!", "id": chamado_id}), 201

    @staticmethod
    def listar_chamados():
        chamados = ChamadoService.listar_chamados()
        resultado = [
            {
                "id": c.id,
                "titulo": c.titulo,
                "descricao": c.descricao,
                "setor": c.setor,
                "status": c.status,
                "prazo": c.prazo.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for c in chamados
        ]
        return jsonify(resultado), 200

    @staticmethod
    def atualizar_chamado(id):
        data = request.json
        status = data.get("status")

        if status not in ["Aberto", "Em Andamento", "Concluído", "Atrasado"]:
            return jsonify({"erro": "Status inválido"}), 400

        ChamadoService.atualizar_status(id, status)
        return jsonify({"mensagem": "Chamado atualizado com sucesso!"}), 200
