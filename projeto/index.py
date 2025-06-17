# FALTOU 14 e 15 (PENDENTE) => 17/06/25
import psycopg2
from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

class ConexaoPostgreSQL:
  def __init__(self):
    pass
  def abreConexao(self):
    return psycopg2.connect("dbname=aula7 user=postgres password=postgres host=localhost")
  def criaPaciente(self, nome, cpf, data_nascimento):
    conn = self.abreConexao()
    cur = conn.cursor()
    sql = "INSERT INTO paciente (nome, cpf, data_nascimento) VALUES (%s, %s, %s);"
    cur.execute(sql, [nome, cpf, data_nascimento])
    conn.commit()
    cur.close()
    conn.close()
  def listar(self):
    conn = self.abreConexao()
    cur = conn.cursor()
    cur.execute("SELECT * FROM consulta")
    records = cur.fetchall()
    cur.close()
    conn.close()
    return records
  
class Medico:
  def __init__(self, crm = None, nome = None, id = 0):
    self.crm = crm
    self.nome = nome
    self.id = id

class Paciente:
  def __init__(self, nome = None, cpf = None, data_nascimento = None, email = None, id = 0):
    self.nome = nome
    self.cpf = cpf    
    self.data_nascimento = data_nascimento
    self.email = email
    self.id = id  

class Consulta:
  def __init__(self, data_hora = None, paciente = None, medico = None, observacao = None, id = 0):
    self.data_hora = data_hora
    self.paciente = paciente
    self.medico = medico
    self.observacao = observacao
    self.id = id

class MedicoDAO:  
  def __init__(self, conexao):
    self.conexao = conexao

  def editar(self, medico):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("UPDATE medico SET crm = %s, nome = %s WHERE id = %s;", [medico.crm, medico.nome, medico.id])
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
      return False
    
  def adicionar(self, medico):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("INSERT INTO medico (crm, nome) VALUES (%s, %s);", [medico.crm, medico.nome])
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
      return False


  def deletar_medico(self, id):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("DELETE FROM medico WHERE id = %s", [int(id)])
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
      return False
   
  def obter(self, id):
    sql = "SELECT * FROM medico WHERE id = %s;"
    conn = self.conexao.abreConexao()
    cur = conn.cursor()
    cur.execute(sql, [id])
    registro = cur.fetchone()
    medico = Medico(registro[1], registro[2], registro[0])
    cur.close()
    conn.close()
    return medico

  def listar_todos(self):
    vetMedico = []
    sql = "SELECT * FROM medico ORDER BY id"
    conn = self.conexao.abreConexao()
    cur = conn.cursor()
    cur.execute(sql)
    for registro in cur.fetchall():
        # print(registro)
        medico = Medico(registro[2], registro[1], registro[0])
        vetMedico.append(medico)
    cur.close()
    conn.close()
    return vetMedico

class PacienteDAO:
  def __init__(self, conexao):
    self.conexao = conexao

  def adicionar(self, paciente):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("INSERT INTO paciente (cpf, nome, data_nascimento, email) VALUES (%s, %s, %s, %s);", [paciente.cpf, paciente.nome, paciente.data_nascimento, paciente.email])
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
      return False

  def listar_todos(self):
    vetPaciente = []
    sql = "SELECT id, nome, mascaraCPF(cpf) as cpf, data_nascimento, email FROM paciente ORDER BY id"
    conn = self.conexao.abreConexao()
    cur = conn.cursor()
    cur.execute(sql)
    for registro in cur.fetchall():
        print(registro[0])
        paciente = Paciente(registro[1], registro[2], registro[3], int(registro[0]))
        # print(paciente)
        vetPaciente.append(paciente)
    cur.close()
    conn.close()
    return vetPaciente
  
  def obter(self, id):
    sql = "SELECT * FROM paciente WHERE id = %s;"
    conn = self.conexao.abreConexao()
    cur = conn.cursor()
    cur.execute(sql, [id])
    registro = cur.fetchone()
    paciente = Paciente(registro[1], registro[2], registro[3], int(registro[0]))
    cur.close()
    conn.close()
    return paciente

class ConsultaDAO:
  def __init__(self, conexao):
    self.conexao = conexao
  
  def listar_todos(self):
    vetConsulta = []
    sql = "SELECT consulta.id, to_char(data_hora, 'DD/MM/YYYY HH:MM'), medico.nome, paciente.nome, observacao FROM consulta INNER JOIN medico ON (consulta.medico_id = medico.id) INNER JOIN paciente on (paciente.id = consulta.paciente_id) ORDER BY id"
    conn = self.conexao.abreConexao()
    cur = conn.cursor()
    cur.execute(sql)
    for registro in cur.fetchall():
        consulta = Consulta(registro[1], registro[3], registro[2], registro[4] if registro[4] != None else "", int(registro[0]))
        vetConsulta.append(consulta)
    cur.close()
    conn.close()
    return vetConsulta

  def adicionar(self, consulta):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("INSERT INTO consulta (data_hora, paciente_id, medico_id, observacao) VALUES (%s, %s, %s, %s);", [consulta.data_hora, consulta.paciente.id, consulta.medico.id, consulta.observacao])
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
      return False
  
  def deletar_consulta(self, id):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("DELETE FROM consulta WHERE id = %s", [int(id)])
      conn.commit()
      cur.close()
      conn.close()
      print("feito!")
      return True
    except Exception as e:
      print(e)
      return False
    
  def atualiza_observacao(self, id, observacao):
    try:
      conn = self.conexao.abreConexao()
      cur = conn.cursor()
      cur.execute("UPDATE consulta SET observacao = %s WHERE id = %s", [observacao, int(id)])
      conn.commit()
      cur.close()
      conn.close()
      return True
    except Exception as e:
      print(e)
      return False

  

@app.route("/")
def index():
  conexao = ConexaoPostgreSQL()
  medicoDAO = MedicoDAO(conexao) 
  vetMedico = medicoDAO.listar_todos()
  vetConsulta = ConsultaDAO(conexao).listar_todos()
  vetPaciente = PacienteDAO(conexao).listar_todos()
  return render_template("index.html", vetPaciente = vetPaciente, vetMedico = vetMedico, vetConsulta = vetConsulta) 



@app.route("/deletar_medico/<int:id>")
def deletar_medico(id):
  conexao = ConexaoPostgreSQL()
  medicoDAO = MedicoDAO(conexao) 
  resultado = medicoDAO.deletar_medico(id)
  return redirect(url_for('index'))

@app.route("/deletar_consulta/<int:id>")
def deletar_consulta(id):
  # print(id)
  conexao = ConexaoPostgreSQL()
  resultado =  ConsultaDAO(conexao).deletar_consulta(id)
  # print(resultado)
  return redirect(url_for('index'))

@app.route("/medico_tela_adicionar")
def medico_tela_adicionar():
  return render_template("medico_tela_adicionar.html")


@app.route("/paciente_tela_adicionar")
def paciente_tela_adicionar():
  return render_template("paciente_tela_adicionar.html")

@app.route("/consulta_tela_adicionar")
def consulta_tela_adicionar():
  vetMedico = MedicoDAO(ConexaoPostgreSQL()).listar_todos()
  vetPaciente = PacienteDAO(ConexaoPostgreSQL()).listar_todos()
  return render_template("consulta_tela_adicionar.html", vetMedico = vetMedico, vetPaciente = vetPaciente)

@app.route("/medico_tela_editar/<int:id>")
def medico_tela_editar(id):
  conexao = ConexaoPostgreSQL()
  medicoDAO = MedicoDAO(conexao) 
  medico = medicoDAO.obter(id)
  return render_template("medico_tela_editar.html", medico=medico)


@app.route("/consulta_tela_editar/<int:id>")
def consulta_tela_editar(id):
  return render_template("consulta_tela_editar.html", consulta_id=id)

def erro(msg):
  return render_template("erro.html", msg=msg)


@app.route("/consulta_adicionar", methods = ['POST'])
def consulta_adicionar():
  consulta = Consulta()
  consulta.data_hora = request.form['data_hora']
  consulta.observacao = request.form['observacao']
  consulta.paciente = PacienteDAO(ConexaoPostgreSQL()).obter(int(request.form['paciente_id']))
  consulta.medico = MedicoDAO(ConexaoPostgreSQL()).obter(int(request.form['medico_id']))
  resultado = ConsultaDAO(ConexaoPostgreSQL()).adicionar(consulta)
  if (resultado is True): 
    return redirect(url_for('index'))
  else:
    return erro("Deu xabum!")

@app.route("/medico_adicionar", methods = ['POST'])
def medico_adicionar():
  medico = Medico()
  medico.crm = request.form['crm']
  medico.nome = request.form['nome']
  conexao = ConexaoPostgreSQL()
  medicoDAO = MedicoDAO(conexao) 
  resultado = medicoDAO.adicionar(medico)
  if (resultado is True): 
    return redirect(url_for('index'))
  else:
    return erro("Deu xabum!")
  

@app.route("/paciente_adicionar", methods = ['POST'])
def paciente_adicionar():
  paciente = Paciente()
  paciente.cpf = request.form['cpf']
  paciente.nome = request.form['nome']
  paciente.data_nascimento = request.form['data_nascimento']  
  paciente.email = request.form['email']
  resultado = PacienteDAO(ConexaoPostgreSQL()).adicionar(paciente)
  if (resultado is True): 
    return redirect(url_for('index'))
  else:
    return erro("Deu xabum!")


@app.route("/medico_editar", methods = ['POST'])
def medico_editar():
  medico = Medico()
  medico.id = int(request.form['id'])
  medico.crm = request.form['crm']
  medico.nome = request.form['nome']
  conexao = ConexaoPostgreSQL()
  medicoDAO = MedicoDAO(conexao) 
  resultado = medicoDAO.editar(medico)
  return redirect(url_for('index'))



@app.route("/consulta_editar", methods = ['POST'])
def consulta_editar():
  consulta_id = int(request.form['id'])
  observacao = request.form['observacao']
  conexao = ConexaoPostgreSQL()
  resultado = ConsultaDAO(conexao).atualiza_observacao(consulta_id, observacao)
  return redirect(url_for('index'))


#  no terminal (linux)
# python3 -m venv .venv
# . .venv/bin/activate
# pip install -r requirements.txt 
# flask --app index run