#ifndef _hdmi_cec_h
#define _hdmi_cec_h

#include <lib/python/connections.h>
#include <lib/driver/rc.h>

class eSocketNotifier;

class eHdmiCEC : public eRCDriver
{
#ifndef SWIG
public:
struct cec_message
{
	unsigned char address;
	unsigned char length;
	unsigned char data[256];
}__attribute__((packed));
#endif
protected:
	static eHdmiCEC *instance;
	int hdmiFd;
	ePtr<eSocketNotifier> messageNotifier;
	void keyPressed(int);
	int translateKey(int kcode);
#ifdef SWIG
	eHdmiCEC();
	~eHdmiCEC();
#endif
public:
#ifndef SWIG
	eHdmiCEC();
	~eHdmiCEC();
#endif
	static eHdmiCEC *getInstance();
	PSignal2<void, int, int> messageReceived;
	void sendMessage(unsigned char address, unsigned char data);
};

class eHdmiCECDevice : public eRCDevice
{
public:
	void handleCode(long code);
	eHdmiCECDevice(eRCDriver *driver);
	const char *getDescription() const;
};

#endif