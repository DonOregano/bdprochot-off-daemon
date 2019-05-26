# yoga311-tweaks
Tweaks necessary for running Linux on the Lenovo Yoga 3-11

Files are located in the relative paths necessary for their use on an Ubuntu 18.04 system.

BD_PROCHOT related tools require the use of the msr module and the msr-tools package:

`sudo apt install msr-tools`

## etc/systemd/system/disable-bd-prochot.service

Copy this file to the same location in the root of your system and run:

`sudo systemctl enable disable-bd-prochot`
`sudo systemctl start disable-bd-prochot`

This will disable BD_PROCHOT at system startup. This is necessary on the Yoga 3-11 because of its *terribly* tuned hardware CPU 
throttling settings. They are well known to be overzealous and, once they've kicked in, they never leave the throttled state on
their own, causing a system to be virtually unusable at around 400-500MHz with no Turbo. This was a well known issue in Windows
which the ThrottleStop software often had to be used to prevent.

## etc/NetworkManager/dispatcher.d/pre-down.d/01_preempt-ath10k-crash

Copy this file to the same location in the root of your system and, if necessary, edit it to reference the correct network 
interface. It will be called by NetworkManager to remove the ath10k_pci module whenever NetworkManager decides to bring down
the interface. 

This is a major kludge, but necessary due to a serious problem with some combinations of adapter firmware and hardware that cause a panic
whenever the interface is brought down. *THE MODULE WILL STILL CRASH*, but it will be appropriately removed prior to that 
panic cascading to the remainder of the system, which is what happens if the network interface is brought down before the module
is unloaded.

It was also necessary to use NetworkManager for this since logind runs and directs NetworkManager before systemd's standby hooks
kick in.

I hang my head in shame at the awfulness of this kludge, but it works for what I need it for.

## lib/systemd/system-sleep/01_disable_bd_prochot

Copy this file to the same location in the root of your system. It will use msr-tools to once again disable the BD_PROCHOT flag
when coming out of standby.

## lib/systemd/system-sleep/02_restore-ath10k-module

Copy this file to the same location in the root of your system. It will reload the ath10k_pci module when coming out of standby.

Enabling at this stage allows NetworkManager to see the interface shortly after and bring it up on its own.

## License / Disclaimer

These scripts are offered with no warranty whatsoever and are licensed in the public domain.
