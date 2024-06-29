SELECT 
 intDeliveryId,
 dteDeliveryDate,
 strSoldToPartnerName,
 strDeliveryTypeName,
 strWarehouseName,
 numCashAmount,
 numCreditAmount,
 numMFSAmount

  
FROM 
 
  [APON].[pos].[tblPosDeliveryHeader] 

  where 
		dteDeliveryDate > '2023-5-01'	