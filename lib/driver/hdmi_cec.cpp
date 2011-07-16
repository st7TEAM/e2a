#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <string.h>

#include <lib/base/init.h>
#include <lib/base/init_num.h>
#include <lib/base/eerror.h>
#include <lib/base/ebase.h>
#include <lib/driver/hdmi_cec.h>

eHdmiCEC *eHdmiCEC::instance = NULL;

eHdmiCEC::eHdmiCEC()
{
	ASSERT(!instance);
	instance = this;
	hdmiFd = ::open("/dev/hdmi_cec", O_RDWR | O_NONBLOCK);
	if (hdmiFd >= 0)
	{
		messageNotifier = eSocketNotifier::create(eApp, hdmiFd, eSocketNotifier::Read);
		CONNECT(messageNotifier->activated, eHdmiCEC::hdmiEvent);
	}
}

eHdmiCEC::~eHdmiCEC()
{
	if (hdmiFd >= 0) ::close(hdmiFd);
}

eHdmiCEC *eHdmiCEC::getInstance()
{
	return instance;
}

void eHdmiCEC::hdmiEvent(int what)
{
	struct cec_message message;
	if (::read(hdmiFd, &message, 2) == 2)
	{
		if (::read(hdmiFd, &message.data, message.length) == message.length)
		{
			/* there is no simple way to pass the complete message object to python, so we support only single byte commands for now */
			messageReceived(message.address, message.data[0]);
			eDebug("[HDMICEC] received from %04x m1 %04x m2 %04x", message.address, message.data[0], message.data[1]);
	
		}
	}
}

void eHdmiCEC::sendMessage(unsigned char address, char *data)
{
	if (hdmiFd >= 0)
	{
		
		__u8 *buf =  new __u8[256];
		unsigned char lenght = 1;

		buf[0] = address;
		buf[2] = 0;
		
		if ( !strcmp((const char*)data, "wake") ) 
		{
			buf[2] = 0x85;
		}
		else if  ( !strcmp((const char*)data, "active") ) 
		{
			buf[2] = 0x04;
		}
		else if  ( !strcmp((const char*)data, "sleep") ) 
		{
			buf[2] = 0x36;
		}
		else if  ( !strcmp((const char*)data, "reportpower") ) 
		{
			buf[2] = 0x90;
			buf[3] = 0x00;
			lenght = 2;
		}
		else if  ( !strcmp((const char*)data, "setname") ) 
		{
			buf[2] = 0x47;
			memcpy(buf+3, "Black Hole", 10);
			lenght = 11;
		}
		else if  ( !strcmp((const char*)data, "reportpaddr") ) 
		{
			buf[2] = 0x84;
			buf[3] = 0x10;
			buf[4] = 0x00;
			buf[5] = 0x03;
			lenght = 3;
		}

		buf[1] = lenght;
		::write(hdmiFd, buf, 2 + lenght);

	}
}

eAutoInitP0<eHdmiCEC> init_hdmicec(eAutoInitNumbers::rc, "Hdmi CEC driver");
