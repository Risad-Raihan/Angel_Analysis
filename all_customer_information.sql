SELECT
	o.strWarehouseName as "Outlet",
	bp.strBusinessPartnerCode as "APON Code",
	bp.strBusinessPartnerName as "Name",
	cinfo.intEmployeeId as "HR Code",
	cinfo.intMaritalStatus as "Marital Status",
	cinfo.intNumberOfFamilyMember as "Number of Family Member",
	bp.strBusinessPartnerAddress as "Address",
	bp.strContactNumber as "Contact Number",
	bp.strEmail as "Email",
	CASE bp.intGenderId
	WHEN 1 THEN 'Male'
	WHEN 2 THEN 'Female'
	END as Gender,
	bp.strNID as "NID",
	bp.DteDateOfBirth as DOB,
	cinfo.strDepartment as 'Department',
	cinfo.strDesignation as 'Designation',
	cinfo.dteJoiningDate as 'Joining Date',
	cinfo.monGrossSalary as 'Gross Salary',
	bp.numDistributorCreditLimit as "Credit Limit",
	SUM(r.numDeliveryValue) as "Total Sales Amount",
	SUM(r.numTotalDiscountValue) as "Total Discount",
	SUM(h.numCashAmount) as "Cash Amount",
	SUM(h.numCreditAmount) as "Credit Amount",
	SUM(h.numCardAmount) as "Card Amount",
	SUM(h.numMFSAmount) as "MFS Amount",
	bp.isActive
  FROM [APON].[prt].[tblBusinessPartner] bp
	LEFT JOIN [APON].[dbo].[CustomerAdditionalInformation] cinfo on bp.intBusinessPartnerId = cinfo.intCustomerId
	LEFT JOIN [APON].[prt].[tblFactoryUnit] as f on cinfo.intFactoryId=f.intFactoryId
	LEFT JOIN [APON].[wms].[tblWarehouse] as o on f.intWarehouseId=o.intWarehouseId
	LEFT JOIN [APON].[pos].[tblPosDeliveryHeader] h on bp.strBusinessPartnerCode = h.strSoldToPartnerCode
	LEFT JOIN [APON].[pos].[tblPosDeliveryRow] r on h.intDeliveryId = r.intDeliveryId

WHERE 
	bp.isActive = 1 AND
	bp.strPartnerSalesType = 'Customer' AND
	cinfo.strFactoryName IS NOT NULL 

GROUP BY
	o.strWarehouseName,
	bp.intBusinessPartnerId,
	bp.strBusinessPartnerCode,
	cinfo.intEmployeeId,
	bp.strBusinessPartnerName,
	cinfo.intMaritalStatus,
	cinfo.intNumberOfFamilyMember,
	bp.strBusinessPartnerAddress,
	bp.strContactNumber,
	bp.strEmail,
	bp.strNID,
	bp.DteDateOfBirth,
	bp.intGenderId,
	cinfo.strDepartment,
	cinfo.strDesignation,
	cinfo.dteJoiningDate,
	cinfo.monGrossSalary,
	bp.numDistributorCreditLimit,
	bp.isActive
ORDER BY
	bp.intBusinessPartnerId