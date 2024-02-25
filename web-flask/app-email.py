from flask import Flask, redirect, url_for
from flask_mail import Mail, Message

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'live.smtp.mailtrap.io'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'api'
app.config['MAIL_PASSWORD'] = 'c372dd794ce8283166bfcc38b84060f5'
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
mail = Mail(app)

@app.route("/")
def root():
    # Redirect to the create_account route with a placeholder email
    return redirect(url_for('create_account', email='michaelmachohi@gmail.com'))
@app.route("/create_account/<email>")
def create_account(email):
    msg = Message(subject='Welcome to Tomorrow - Your Journey Starts Now!',
                  sender='mailtrap@holb20233m8xq2.tech',
                  recipients=[email],
                  html="""<html>
                          <head>
                              <style>
                                  body {
                                      font-family: 'Arial', sans-serif;
                                      max-width: 600px;
                                      margin: auto;
                                      padding: 20px;
                                  }
                                  img {
                                      display: block;
                                      margin: auto;
                                      max-width: 100%;
                                  }
                                  p {
                                      text-align: justify;
                                  }
                                  .footer {
                                      margin-top: 20px;
                                      text-align: center;
                                      color: #777;
                                  }
                                  .title {
                                      text-align: left;
                                      font-size: 1.5rem;
                                      color:#777;
                                  }
                              </style>
                          </head>
                          <body>
                            <p>Dear [User],</p>
                            <p>We hope this email finds you well.<p>
                                
                            <h1 class="title">Welcome to Tomorrow</h1>
                              <img src="https://web-01.holb20233m8xq2.tech/images/Light-purple.png" alt="Tomorrow Logo">
                              <p>We're thrilled to have you on board, and your journey towards a brighter, more organized future begins right now.</p>
                              <p>Picture a stress-free tomorrow where your tasks effortlessly align with your goals. That's the Tomorrow experience we're excited to bring to you.</p>
                              <p>Incase of any enquiries, feel free to 
                                <a href="mailto:tomorrow.clientdesk@gmail.com">contact us</a>
                              </p>
                              <p>Thank you for choosing Tomorrow.</p>
                              <p class="footer">Best regards,<br>The Tomorrow Team</p>
                          </body>
                          </html>""")
    mail.send(msg)
    return "Account creation email sent to {}".format(email)

if __name__ == '__main__':
    app.run(debug=True)
