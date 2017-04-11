#!/usr/bin/env python3
import sys
import magic
import argparse
import smtplib
#from time import sleep
from os.path import basename
from os.path import isfile
from email.parser import Parser
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

class Email:
    """ 
        Attributes:
        Most ot them self explanatory as they are email headers
        dsnOptions: by default, FAILURE is always on
        attachmentList: List of file paths to attachments
        body: Text body
        htmlBody: HTML Body to be displayed if client allows it
    """
    def __init__(self, mailFrom):
        """ body can be a string or a file path.  It checks if the file path exists, if not it will treat it as a string """

        self.mailFrom = mailFrom.getHeader()

        self.rcptTo = []

        self.cc = []

        self.bcc = []

        self.attachmentList = []

        self.dsnOptions = ""

        self.body = ""

        self.htmlBody = ""

        self.subject = ""
                 

    def __str__(self):
        attr = []
        for key in self.__dict__:
            attr.append("{key}='{value}'".format(key=key, value=self.__dict__[key]))
        return ('\n'.join(map(str, attr))) 
    
    __repr__ = __str__

    def addSubject(self,subject):
        self.subject = subject

    def addBody(self,body):
        if not (body is None):
            try:
                with open (body, "r") as emailBody:
                    self.body = emailBody.read()
            except IOError:
                self.body = body

    def addHtmlBody(self, htmlBody):
        if not (htmlBody is None):
            try:
                with open (htmlBody, "r") as emailBody:
                    self.htmlBody = emailBody.read()
            except IOError:
                print ("Can not open htmlBody file:", htmlBody)        

    def addDsnOptions(self, success, delay, failure):
        """ Adds SUCCESS and/or DELAY to the string to be passed as rcpt_options """
        options = []
        if (success or delay or failure):
            self.dsnOptions = "NOTIFY="
            if success:
                options.append("SUCCESS")
            if delay:
                options.append("DELAY")
            if failure:
                options.append("FAILURE")
            self.dsnOptions += ','.join(filter(None,options))

    def addAttachment(self, attachment):
        if attachment not in self.attachmentList:
            self.attachmentList.append(attachment)

    def clearAttachment(self):
        self.attachments.clear()

    def addRcptTo(self, address):
        if address.getHeader() not in self.rcptTo:
            self.rcptTo.append(address.getHeader())

    def getRcptTo(self):
        return self.rcptTo
        
    def clearRcptTo(self):
        self.rcptTo.clear()

    def addCc(self, address):
        if address.getHeader() not in self.cc:
            self.cc.append(address.getHeader())

    def clearCc(self):
        self.cc.clear()

    def addBcc(self, bcc, bccName=None):
        if address.getHeader() not in self.bcc:
            self.bcc.append(address.getHeader())

    def clearBcc(self):
        self.bcc.clear()

    def send(self,smtpHost, verbose, noTls, testPrint):
        """ 
            Create an actual smtplib object and send it to smtpHost
            testPrint: only prints the message without sending it
            verbose: outputs debug info 
        """
        
        msg = MIMEMultipart('alternative')
        msg.attach(MIMEText(self.body, 'plain'))
        if self.htmlBody:
            msg.attach(MIMEText(self.htmlBody, 'html'))
                
        if any(self.attachmentList):
            for attachment in self.attachmentList:
                fileAttach = attachment.convertToMime()
                msg.attach(fileAttach)
        
        msg['From'] = self.mailFrom
        
        if self.rcptTo:
            msg['To'] = ','.join(self.rcptTo)
        if self.cc:
            msg['cc'] = ','.join(self.cc)
        if self.bcc:
            msg['bcc'] = ','.join(self.bcc)
        if self.subject:
            msg['Subject'] = self.subject

        if testPrint:
            print(msg.as_string())
        else:
            smtpConnection = smtplib.SMTP(smtpHost)
            if not noTls:
            	smtpConnection.starttls()
            if verbose:
                smtpConnection.set_debuglevel(1)
            if self.dsnOptions:
                msg['Disposition-Notification-To'] = self.mailFrom
                smtpConnection.send_message(msg, rcpt_options=[self.dsnOptions])
            else:
                smtpConnection.send_message(msg)
            smtpConnection.quit()


class EmailAddress:
    """ 
        Attributes:
        address: email address john@doe.com 
        name: Full Name "John Doe"
        header: "John Doe"<john@doe.com>
    """
    def __init__(self, address):

        if (len(address) == 1):
            self.address = address[0]
            self.name = address[0]
        elif (len(address) == 2):
            self.address = address[0]
            self.name = address[1]
        
        self.header = "\"" + self.name + "\" <" + self.address + ">"

    def getAddress(self):
        return self.address

    def getName(self):
        return self.name

    def getHeader(self):
        return self.header

    def __str__(self):
        return "Address: " + self.address + " Name: " + self.name + " Header: " + self.header 
    
    __repr__ = __str__


class Attachment:
    def __init__(self, filepath):
        self.attachmentFilePath = ""
        self.attachmentFileName = ""
        self.attachmentMimeType = ""

        if isfile(filepath):
            self.attachmentFilePath = filepath
            self.attachmentFileName = basename(filepath)
            mime = magic.Magic(mime=True)
            self.attachmentMimeType = mime.from_file(filepath)
        else:    
            print(filepath,"is not a valid file path")
            sys.exit(0)

    def getFilePath(self):
        return self.attachmentFilePath

    def getFileName(self):
        return self.attachmentFileName

    def convertToMime(self):
        """
            Returns a MIME Object with the file stream + Content-Disposition headers
        """
        with open(self.attachmentFilePath, 'rb') as fp:
            fileAttach = MIMEApplication(fp.read(),name=(self.attachmentFileName))
        fileAttach['Content-Disposition'] = 'attachment; filename="%s"' % self.attachmentFileName
        return fileAttach

    def __str__(self):
        return "File path: " + self.attachmentFilePath + " MIME Type: " + self.attachmentMimeType

    __repr__ = __str__

class AddEmailAddresses(argparse._AppendAction):
    """
        Extends append action for parser.  Needed to validate email addresses (address and Full name)
    """
    def __call__(self, parser, namespace, values, option_string=None):
        #Todo: Add email address validation
        if not (1 <= len(values) <= 2):
            raise argparse.ArgumentError(self, "Only accepts one email address and an optional Full Name")
        super(AddEmailAddresses, self).__call__(parser, namespace, values, option_string)

def main():
    parser = argparse.ArgumentParser('Imeil')
    parser.add_argument("-f", "--mailfrom", nargs='+', action=AddEmailAddresses, dest="mailfrom", metavar=('address','Full Name'), help="Mail From: ")
    parser.add_argument("-m", "--smtphost", dest="smtphost", help="SMTP server where to send feed")
    parser.add_argument("-s", "--subject", dest="subject", help="Subject")
    parser.add_argument("-b", "--body", dest="body", help="text/plain body - String or path to the file containing the body")
    parser.add_argument("-l", "--htmlbody", dest="html", help="text/html body - String or path to the file containing the html body")
    parser.add_argument("-r", "--rcptto", nargs='+', action=AddEmailAddresses, dest="rcptto",metavar=('address','Full Name'), help="RCPT TO: ")
    parser.add_argument("-c", "--cc", nargs='+', action=AddEmailAddresses, dest="cc", metavar=('address','Full Name'), help="CC: ")
    parser.add_argument("-o", "--bcc", nargs='+', action=AddEmailAddresses, dest="bcc", metavar=('address','Full Name'), help="BCC: ")
    parser.add_argument("-u", "--success", action='store_true', default=False, dest="success", help="Success Notification to be sent from the server")
    parser.add_argument("-d", "--delay", action='store_true', default=False, dest="delay", help="Delay Notification to be sent from the server")
    parser.add_argument("-i", "--failure", action='store_true', default=False, dest="failure", help="Failure Notification to be sent from the server")
    parser.add_argument("-a", "--attach", nargs='+', action='append', dest="attachments", help="Path to files to attach")
    parser.add_argument("-p", "--print", action='store_true', default=False, dest="testprint", help="Prints the message instead of sending it")
    parser.add_argument("-t", "--notls", action='store_true', default=False, dest="notls", help="Disables TLS")
    parser.add_argument("-v", "--verbose", action='store_true', default=False, dest="verbose", help="Verbose")

    args = parser.parse_args()

    if(len(sys.argv)==1):
        parser.print_help()
        sys.exit(0)

    for listMailFrom in args.mailfrom:
        mailFromAddress = EmailAddress(listMailFrom)
        correo = Email(mailFromAddress)
        correo.addDsnOptions(args.success,args.delay,args.failure)

        if args.subject:
            correo.addSubject(args.subject)
        if args.body:
            correo.addBody(args.body)
        if args.html:
            correo.addHtmlBody(args.html)
        if args.rcptto:
            for listRcptTo in args.rcptto:
                rcptToAddress = EmailAddress(listRcptTo)
                correo.addRcptTo(rcptToAddress)
        if args.cc:
            for listCc in args.cc:
                ccAddress = EmailAddress(listCc)
                correo.addCc(ccAddress)
        if args.bcc:
            for listBcc in args.bcc:
                bccAddress = EmailAddress(listBcc)
                correo.addBcc(bccAddress)
        if args.attachments:
            for filepath in args.attachments:
                correo.addAttachment(Attachment(filepath[0]))

    correo.send(args.smtphost, args.verbose, args.notls, args.testprint)
  

if __name__ == "__main__":
    main()