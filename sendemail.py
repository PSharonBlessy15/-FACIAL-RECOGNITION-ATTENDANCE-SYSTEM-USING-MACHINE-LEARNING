import smtplib

def send(name,status,studentid,dtime,s):
  msg = "Greetings Sir/Madam                             Your ward "+name+ " is "+status+" for today's class."
  if(s):
     msg+="He/She has entered the class at "
     msg+=dtime[0]
     msg+=" "
     msg+= dtime[1]
     msg+=" AM ."


  server=smtplib.SMTP('smtp.gmail.com',587)

  server.starttls()

  server.login('harshinimani2022@gmail.com','qgqmaxmgketkqiii')

  server.sendmail('harshinimani2022@gmail.com',studentid,msg)

  print('mail sent')





