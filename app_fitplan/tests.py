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

    def test_fluxo_treino(self):
        self.driver.get(f'{self.live_server_url}/cadastro/')
        time.sleep(4)
        self.driver.find_element(By.NAME, 'username').send_keys('usuario_generico')
        self.driver.find_element(By.NAME, 'nome_completo').send_keys('Usuário Genérico')
        self.driver.find_element(By.NAME, 'email').send_keys('usuario@test.com')
        self.driver.find_element(By.NAME, 'password').send_keys('12345')
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)
        self.assertIn('login', self.driver.current_url)

        self.driver.get(f'{self.live_server_url}/login/')
        time.sleep(4)
        self.driver.find_element(By.NAME, 'email').send_keys('usuario_generico')
        self.driver.find_element(By.NAME, 'password').send_keys('12345')
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)
        self.assertIn('menu', self.driver.current_url)

        # Fluxo 1 - Treinar
        self.driver.get(f'{self.live_server_url}/intensidade/')
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//button[@value='Leve']").click()
        time.sleep(4)
        self.assertIn('duracao', self.driver.current_url)

        self.driver.find_element(By.XPATH, "//button[@value='45MIN']").click()  
        time.sleep(4)
        self.assertIn('local', self.driver.current_url)

        self.driver.find_element(By.XPATH, "//button[@value='Na academia']").click()
        time.sleep(4)
        self.assertIn('agrupamento_muscular', self.driver.current_url)

        self.driver.find_element(By.XPATH, "//button[@value='Peito e tríceps']").click()
        time.sleep(4)
        self.assertIn('gerar_treino', self.driver.current_url)

        # Selecionar treino como favorito
        self.driver.find_element(By.XPATH, "//button[contains(text(), 'Favoritar')]").click()
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Verificar Treinos Favoritados
        self.driver.get(f'{self.live_server_url}/favoritos/')
        time.sleep(4)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'favoritos-container').is_displayed())
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Verificar Histórico de Treinos
        self.driver.get(f'{self.live_server_url}/historico_treinos/')
        time.sleep(4)
        self.assertTrue(self.driver.find_element(By.CLASS_NAME, 'historico-container').is_displayed())
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Limpar dados e iniciar nova sessão
        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_acompanhamento_progresso(self):
        self.driver.get(f'{self.live_server_url}/progresso/')
        time.sleep(4)
        image_path = r'C:\Users\Caio\Desktop\tudo FDS\boneco-fds.jpg'
        self.driver.find_element(By.NAME, 'imagem').send_keys(image_path)
        data_field = self.driver.find_element(By.NAME, 'data')
        self.driver.execute_script("arguments[0].value = '2024-10-20';", data_field)
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Limpar dados e iniciar nova sessão
        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_calculadora_imc(self):
        self.driver.get(f'{self.live_server_url}/calculadora-imc/')
        time.sleep(4)
        self.driver.find_element(By.NAME, 'peso').send_keys('75')
        self.driver.find_element(By.NAME, 'altura').send_keys('1.80')
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Limpar dados e iniciar nova sessão
        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_medidas(self):
        self.driver.get(f'{self.live_server_url}/medidas/')
        time.sleep(4)
        self.driver.find_element(By.NAME, 'peso').send_keys('80')
        self.driver.find_element(By.NAME, 'altura').send_keys('1.75')
        self.driver.find_element(By.NAME, 'cintura').send_keys('90')
        self.driver.find_element(By.NAME, 'quadril').send_keys('100')
        data_field = self.driver.find_element(By.NAME, 'data')
        self.driver.execute_script("arguments[0].value = '2024-10-20';", data_field)
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//button[@type='submit']").click()
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Limpar dados e iniciar nova sessão
        self.limpar_dados()
        self.iniciar_nova_sessao()

    def test_fluxo_dicas_alimentares(self):
        self.driver.get(f'{self.live_server_url}/dicas-alimentares/')
        time.sleep(4)
        self.driver.find_element(By.XPATH, "//div[text()='Manutenção da saúde']").click()
        time.sleep(4)
        dicas = self.driver.find_element(By.ID, 'dicas-container')
        self.assertTrue(dicas.is_displayed())
        time.sleep(4)
        self.driver.find_element(By.LINK_TEXT, "Voltar ao Menu").click()
        time.sleep(4)

        # Limpar dados e iniciar nova sessão
        self.limpar_dados()
        self.iniciar_nova_sessao()