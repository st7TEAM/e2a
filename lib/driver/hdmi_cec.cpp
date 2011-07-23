/******************************************************************************
 *                          <<< Hdmi CEC Driver >>>                           *
 *                                                                            *
 *                     (c) 2011 Amedeo de Longis "meo"                        *
 *                          Licensed under the GPL                            *
 *                                                                            *
 ******************************************************************************/
#include <unistd.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <string.h>

#include <linux/input.h>
#include <lib/base/init.h>
#include <lib/base/init_num.h>
#include <lib/base/eerror.h>
#include <lib/base/ebase.h>
#include <lib/driver/input_fake.h>
#include <lib/base/nconfig.h>
#include <lib/driver/hdmi_cec.h>

eHdmiCEC *eHdmiCEC::instance = NULL;
int last = 0;

eHdmiCEC::eHdmiCEC(): eRCDriver(eRCInput::getInstance())
{
	ASSERT(!instance);
	instance = this;
	hdmiFd = ::open("/dev/hdmi_cec", O_RDWR | O_NONBLOCK);
	if (hdmiFd >= 0)
	{
		messageNotifier = eSocketNotifier::create(eApp, hdmiFd, eSocketNotifier::Read);
		CONNECT(messageNotifier->activated, eHdmiCEC::keyPressed);
		
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

void eHdmiCEC::sendMessage(unsigned char address, unsigned char data)
{
	if (hdmiFd >= 0)
	{
		__u8 *buf =  new __u8[256];
		std::string configvalue;
		unsigned char phys = 0x10;
		unsigned char phys2 = 0x00;
                int port = 0;

		if (!ePythonConfigQuery::getConfigValue("config.hdmicec.port", configvalue))
		{
			port = atoi(configvalue.c_str());
		}

		switch (port)
		{
			case 2:
				phys = 0x20;
				break;
			case 3:
				phys = 0x30;
				break;
			case 4:
				phys = 0x40;
				break;
			case 5:
				phys = 0x11;
				break;
			case 6:
				phys = 0x21;
				break;
			case 7:
				phys = 0x31;
				break;	
			case 8:
				phys = 0x41;
				break;
			case 9:
				phys = 0x22;
				break;
			default:
				phys = 0x10;
				break;
		}

		buf[0] = address;
		buf[1] = 1;
		buf[2] = data;
		
		switch (data)
		{
			case 0x82:
				buf[1] = 3;
				buf[3] = phys;
				buf[4] = phys2;
				break; /* active  */
			case 0x90:
				buf[1] = 2;
				buf[3] = 0x00;
				break; /* reportpower  */
			case 0x47:
				buf[1] = 11;
				memcpy(buf+3, "BlackHole", 10);
				break; /* setname  */
			case 0x84:
				buf[1] = 4;
				buf[3] = phys;
				buf[4] = phys2;
				buf[5] = 3;
				break; /* reportaddress  */
			case 0x8E:
				buf[1] = 2;
				buf[3] = 0;
				break; /* menuon  */

		}
		
		::write(hdmiFd, buf, 2 + buf[1]);
//		eDebug("[BlackHole-HDMICEC] message sent to %02x: %02x %02x %02x %02x", buf[0], buf[2], buf[3], buf[4], buf[5]);
	}

}

void eHdmiCEC::keyPressed(int)
{
	struct cec_message message;
	long code;
	int key;
	unsigned char address; 
	unsigned char data;


	std::string configvalue;
	bool hdmion = (ePythonConfigQuery::getConfigValue("config.hdmicec.on", configvalue) >= 0 && configvalue == "True");
//	eDebug("[BlackHole-HDMICEC] Hdmicec config : %d", hdmion);
	
	if (hdmion == true)
	{ 
	    if (::read(hdmiFd, &message, 2) == 2)
	    {
		if (::read(hdmiFd, &message.data, message.length) == message.length)
		{
			/* pass message object to python */
			messageReceived(message.address, message.data[0]);
//			eDebug("[BlackHole-HDMICEC] received from %02x command: %02x %02x %02x %02x", message.address, message.data[0], message.data[1], message.data[2], message.data[3]);
			
			if (message.data[0] == 0x44 || message.data[0] == 0x45)
			{
				last = 1;
				if (message.data[0] == 0x45)
					last = 0;
					
				key = message.data[1];
				code = translateKey(key);
				for (std::list<eRCDevice*>::iterator i(listeners.begin()); i!=listeners.end(); ++i)
				{
					(*i)->handleCode(code);
				}
			} else
			{
				// We have to reply
				switch (message.data[0])
				{
					case 0x46:
						address = 0;
						data = 0x47; /* setname */
						break;
					case 0x8f:
						address = 0;
						data = 0x90; /* reportpower */
						break;
					case 0x83:
						address = 0x0F;
						data = 0x84; /* reportaddress */
						break;
					case 0x86:
						address = 0x0F;
						data = 0x84; /* reportaddress */
						break;
					case 0x85:
						address = 0x0F;
						data = 0x82; /* active source */
						break;
					case 0x8d:
						address = 0;
						data = 0x8E; /* menuon */
						break;
					default:
						data = 0;
						break;

				}
				if(data != 0)
					sendMessage(address, data);
					
			}
		}
	    }
	}
}

int eHdmiCEC::translateKey(int kcode)
{
	int key = 0;
	switch (kcode)
	{
		case 0x32:
			key = 0x8b;
			break;
		case 0x20:
			key = 0x0b;
			break;
		case 0x21:
			key = 0x02;
			break;
		case 0x22:
			key = 0x03;
			break;
		case 0x23:
			key = 0x04;
			break;
		case 0x24:
			key = 0x05;
			break;
		case 0x25:
			key = 0x06;
			break;
		case 0x26:
			key = 0x07;
			break;
		case 0x27:
			key = 0x08;
			break;
		case 0x28:
			key = 0x09;
			break;
		case 0x29:
			key = 0x0a;
			break;
		case 0x30:
			key = 0x192;
			break;
		case 0x31:
			key = 0x193;
			break;
		case 0x53:
			key = 0x166;
			break;
		case 0x00:
			key = 0x160;
			break;
		case 0x03:
			key = 0x69;
			break;
		case 0x04:
			key = 0x6a;
			break;
		case 0x01:
			key = 0x67;
			break;
		case 0x02:
			key = 0x6c;
			break;
		case 0x0d:
			key = 0xae;
			break;
		case 0x72:
			key = 0x18e;
			break;
		case 0x71:
			key = 0x191;
			break;
		case 0x73:
			key = 0x18f;
			break;
		case 0x74:
			key = 0x190;
			break;

		default:
			key = 0x8b;
			break;
	}
	return key;
}

void eHdmiCECDevice::handleCode(long code)
{
	
	switch (last)
	{
	case 0:
		/*emit*/ input->keyPressed(eRCKey(this, code, eRCKey::flagBreak));
		break;
	case 1:
		/*emit*/ input->keyPressed(eRCKey(this, code, 0));
		break;
	case 2:
		/*emit*/ input->keyPressed(eRCKey(this, code, eRCKey::flagRepeat));
		break;
	}

}

eHdmiCECDevice::eHdmiCECDevice(eRCDriver *driver)
			: eRCDevice("Hdmi-Cec", driver)
{
}


const char *eHdmiCECDevice::getDescription() const
{
	return "Black Hole Hdmi-Cec";
}

class eHdmiCECInit
{
	eHdmiCEC driver;
	eHdmiCECDevice device;

public:
	eHdmiCECInit(): driver(), device(&driver)
	{
	}
};

eAutoInitP0<eHdmiCECInit> init_hdmicec(eAutoInitNumbers::rc+1, "Hdmi CEC driver");
