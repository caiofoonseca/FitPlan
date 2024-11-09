import time
from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from .models import Progresso, Medida, Treino, Favorito

class FitPlanSeleniumTests(LiveServerTestCase):

    def setUp(self):
        chrome_options = Options()
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.implicitly_wait(10)

    def tearDown(self):
        self.driver.quit()

    def limpar_dados(self):
        Progresso.objects.all().delete()
        Medida.objects.all().delete()
        Treino.objects.all().delete()
        Favorito.objects.all().delete()

    def iniciar_nova_sessao(self):
        self.tearDown()
        self.setUp()

    def cadastro_login(self, usuario, email):
        self.driver.get(f'{self.live_server_url}/cadastro/')
        time.sleep(1)
        self.driver.find_element(By.NAME, 'username').send_keys(usuario)
        self.driver.find_element(By.NAME, 'nome_completo').send_keys('Usuário Genérico')
        self.driver.find_element(By.NAME, 'email').send_keys(email)
        self.driver.find_element(By.NAME, 'password').send_keys('12345')
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)

        self.driver.get(f'{self.live_server_url}/login/')
        time.sleep(1)
        self.driver.find_element(By.NAME, 'email').send_keys(usuario)
        self.driver.find_element(By.NAME, 'password').send_keys('12345')
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)

    def test_fluxo_treino(self):
        self.cadastro_login("usuario_treino", "usuario_treino@test.com")

        self.driver.get(f'{self.live_server_url}/intensidade/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@value='Leve']").click()
        time.sleep(2)
        
        self.driver.get(f'{self.live_server_url}/duracao/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@value='1HR']").click()
        time.sleep(2)
        
        self.driver.get(f'{self.live_server_url}/local/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@value='Na academia']").click()
        time.sleep(2)
        
        self.driver.get(f'{self.live_server_url}/agrupamento_muscular/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@value='Peito e tríceps']").click()
        time.sleep(2)

        self.driver.get(f'{self.live_server_url}/gerar_treino/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//a[contains(@href, 'favoritar_exercicio')]").click()
        time.sleep(2)

        self.driver.get(f'{self.live_server_url}/menu/')
        time.sleep(2)
        self.driver.get(f'{self.live_server_url}/favoritos/')
        time.sleep(2)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'favorito-list').is_displayed())
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(2)

        self.driver.get(f'{self.live_server_url}/historico_treinos/')
        time.sleep(2)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'treino-list').is_displayed())
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(2)

        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_acompanhamento_progresso(self):
        self.cadastro_login("usuario_progresso", "usuario_progresso@test.com")

        self.driver.get(f'{self.live_server_url}/progresso/')
        time.sleep(1)
        image_path = r'C:\Users\Caio\Desktop\tudo FDS\boneco-fds.jpg'
        self.driver.find_element(By.NAME, 'imagem').send_keys(image_path)
        data_field = self.driver.find_element(By.NAME, 'data')
        self.driver.execute_script("arguments[0].value = '2024-10-20';", data_field)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(1)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(1)

        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_calculadora_imc(self):
        self.cadastro_login("usuario_imc", "usuario_imc@test.com")

        self.driver.get(f'{self.live_server_url}/calculadora-imc/')
        time.sleep(2)
        self.driver.find_element(By.NAME, 'peso').send_keys('75')
        self.driver.find_element(By.NAME, 'altura').send_keys('1.80')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(2)

        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_medidas(self):
        self.cadastro_login("usuario_medidas", "usuario_medidas@test.com")

        self.driver.get(f'{self.live_server_url}/medidas/')
        time.sleep(2)
        self.driver.find_element(By.NAME, 'peso').send_keys('80')
        self.driver.find_element(By.NAME, 'altura').send_keys('1.75')
        self.driver.find_element(By.NAME, 'cintura').send_keys('90')
        self.driver.find_element(By.NAME, 'quadril').send_keys('100')
        data_field = self.driver.find_element(By.NAME, 'data')
        self.driver.execute_script("arguments[0].value = '2024-10-20';", data_field)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(2)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(2)

        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_dicas_alimentares(self):
        self.cadastro_login("usuario_dicas", "usuario_dicas@test.com")

        self.driver.get(f'{self.live_server_url}/dicas-alimentares/')
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[contains(text(), 'Manutenção da Saúde')]").click()
        time.sleep(2)

        dicas_container = self.driver.find_element(By.ID, 'dicas-container')
        self.assertTrue(dicas_container.is_displayed())
        time.sleep(2)

        dicas_texto = dicas_container.find_elements(By.TAG_NAME, 'p')
        self.assertGreater(len(dicas_texto), 0)  
        time.sleep(2)

        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(2)

        self.limpar_dados()
        self.iniciar_nova_sessao()