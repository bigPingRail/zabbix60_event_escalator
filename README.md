
# zabbix60_event_escalator
### Description:
This is python script used to change event severity in zabbix 6.0
the script use jsonrpc2.0 calls to zabbix server

### Prerequisites:
zabbix 6 server  
python >= 3.6  

### Usage:
1. Place this script to zabbix 6 server
2. Generate new API token in zabbix    
3. Create Environment variable `ESCALATOR_TOKEN=<your_token_value>` on zabbix server 
4. Create new action in Admin section
	 1. Name: `Event Escalator` (for example) 
	 2. Type: `Script`
	 3. Execute on: `Zabbix server`  
	 4. Commands: `/path/to/python3 /path/to/zabbix_event_escalator.py -e {EVENT.ID}`
	 5. Host Group: All (for exmaple)  
5. Use this in action step 
