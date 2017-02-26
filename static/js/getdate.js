var today = new Date;
var current_year = today.getFullYear();
var current_month = today.getMonth();


function countPeriod(m_start, y_start, m_end, y_end)
{
	
	var months = 12*(y_end - y_start) + m_end - m_start;
	var month_num = months % 12;
	var year_num = Math.floor(months/12);
	
	return  [year_num, month_num];
}

function isPlural(num)
{
	if (num>1) return 's';
	else return '';
}

function showPeriod(m_start, y_start, m_end, y_end)
{
	var period = countPeriod(m_start, y_start, m_end, y_end);
	if (period[0]==0)
	{
		return period[1]+" month"+isPlural(period[1]);
	}
	else if (period[1]==0)
	{
		return period[0]+" year"+isPlural(period[0]);
	}
	else
	{
		return period[0]+" year"+isPlural(period[0])+ " "+ period[1]+" month"+isPlural(period[1]);	
	}
}

function setText(id_name, text)
{
	var node = document.getElementById(id_name);
	node.innerText = text;

}

setText("current_year", new Date().getFullYear());
setText("last_period", showPeriod(3,2013, new Date().getMonth(), new Date().getFullYear()));
setText("total_period", showPeriod(8, 2011, new Date().getMonth(), new Date().getFullYear()));

