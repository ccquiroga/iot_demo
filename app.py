import web
from web import form
import pymysql

urls = (
    '/', 'Index'
)

app = web.application(urls, globals())

render = web.template.render('templates', base='base')

class Index:
    conn = pymysql.connect(host="wp433upk59nnhpoh.cbetxkdyhwsb.us-east-1.rds.amazonaws.com", port=3306, user="nwc6tssdqmori2cr", passwd="t6ifbjox2d6t2d5y", db="arduino")
    cur = conn.cursor()

    control = form.Form(
        form.Button("Encender/Apagar", type = "submit", description = "Encender/Apagar")
    )

    def GET(self):
        data = 0
        control = 0
        formulario = self.control()
        self.cur.execute("SELECT * FROM data order by id desc limit 1")
        for row in self.cur:
            data = row[2]
        
        self.cur.execute("SELECT * FROM control order by id desc limit 1")
        for row in self.cur:
            control = row[2]

        return render.index(data, control, formulario)

    def POST(self):
        formulario = self.control()
        if not formulario.validates():
            pass
        else:
            self.cur.execute("SELECT * FROM control order by id desc limit 1")
            for row in self.cur:
                control = row[2]
            print control
            value = control
            if value == 1:
                value = 0
            else:
                value= 1
            self.cur.execute("update control set value = "+str(value)+" where id = 1")
            self.conn.commit()
            raise web.seeother("/")

if __name__ == '__main__':
    web.config.debug = False
    app.run()
