import pywinauto, time 
from pywinauto.application import Application
from pywinauto.keyboard import send_keys

async def abre_zoom():
    try:
        app = Application(backend='uia').start(cmd_line=u'"C:\\Users\\guico\\AppData\\Roaming\\Zoom\\bin\\Zoom.exe"').connect(title='Zoom', timeout=5)
        app.Zoom.child_window(title="Start a new meeting with video off", control_type="Button").click()

        meeting = Application(backend='uia').connect(title='Zoom Meeting', timeout=10)
        meeting.ZoomMeeting.Maximizar.click()
        time.sleep(1)
        security = meeting.ZoomMeeting.child_window(title="Security", control_type="MenuItem")
        security.select()
        time.sleep(1)
        security.type_keys('{VK_DOWN}')
        security.type_keys('{VK_DOWN}')
        security.type_keys('{ENTER}')

        time.sleep(120)
        send_keys('%q')
        send_keys('{VK_TAB}')
        send_keys('{ENTER}')
        time.sleep(1)

        try:
            end_meeting = Application(backend='uia').connect(title='End Meeting or Leave Meeting?', timeout=10)
            end_meeting.LeaveMeeting.child_window(title="Assign and Leave", control_type="Button").click()

            app.kill()
            return "Fim dos 2 minutos. Eu saí da reunião."
        except:
            app.kill()
            return 'Ninguem entrou na sala. Fim da reunião.'

    except:
        try:
            try:
                Application(backend='uia').connect(title='Zoom Meeting', timeout=5)
                send_keys('%q')
                send_keys('{ENTER}')
                time.sleep(1)
                end_meeting = Application(backend='uia').connect(title='End Meeting or Leave Meeting?', timeout=10)
                end_meeting.LeaveMeeting.child_window(title="Assign and Leave", control_type="Button").click()
                time.sleep(1)
                app.kill()
                return "Um erro ocorreu, ou já existe uma reunião em execução. [0]"
            except:
                Application(backend='uia').connect(title='Zoom Meeting 40 Minutes', timeout=5).kill()
                send_keys('%q')
                send_keys('{ENTER}')
                time.sleep(1)
                end_meeting = Application(backend='uia').connect(title='End Meeting or Leave Meeting?', timeout=10)
                end_meeting.LeaveMeeting.child_window(title="Assign and Leave", control_type="Button").click()
                time.sleep(1)
                app.kill()
                return "Um erro ocorreu, ou já existe uma reunião em execução. [1]"
        except:
            app.kill()
            return "Um erro ocorreu, ou já existe uma reunião em execução. [2]"
            
        