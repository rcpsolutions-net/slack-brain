SELECT cc.companyName, * FROM ClientCorporation c, ClientContact cc
WHERE 
c.clientCorporationID = cc.clientCorporationID AND
cc.companyName LIKE '%Personnel %'
