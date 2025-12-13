const onDOMLoad = () => {

  // Update the customer name in the footer
  updateCustomerName('Pied Piper Inc.');

  // Update the creation date in the footer
  const timestamp = new Date().toLocaleString('en-us',{ month:'short', day: 'numeric', year:'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
  
  updateCreationDate(timestamp);

  updateReportNameInFooter("Imperva API Report")
  
  // Update circular progress bar charts under
  // Frequently occuring violations
  renderCircularProgressBar("violationMetric1", 30);
};

/**
 * Function to render circular progress bar for
 * Most Frequently Occuring Violations
 */
const renderCircularProgressBar = (chartId, value) => {
  const data = {
    labels: ["Test"],
    datasets: [
      {
        label: "My First Dataset",
        data: [value, 100 - value],
        backgroundColor: ["#285AE6", "#ACB9C5"],
        borderWidth: 0,
        hoverOffset: 4,
      },
    ],
  };

  const config = {
    type: "doughnut",
    data: data,
    options: {
      hover: { mode: null },
      cutout: "75%",
      plugins: {
        legend: false,
        tooltip: {
          enabled: false,
        },
      },
    },
  };

  const myChart = new Chart(
    document.getElementById(chartId),
    config
  );

  const percentageTextElement = document.querySelector(`#${chartId} + .violation-donut-percentage`);

  percentageTextElement.textContent = value + "%";
};

/**
 * Function to update report name in the footer section
 */
const updateReportNameInFooter = (reportName) => {
  const elementsList = document.querySelectorAll(".report-name");
  
  elementsList.forEach(element => {
    element.textContent = reportName;
  });
}

/**
 * Function to update customer name in the footer section
 */
const updateCustomerName = (name) => {
  const elementsList = document.querySelectorAll(".customer");
  
  elementsList.forEach(element => {
    element.textContent = `For: ${name}`;
  });
}

/**
 * Function to update the creation date in the footer section
 */
const updateCreationDate = (dateString) => {
  const elementsList = document.querySelectorAll(".date");
  
  elementsList.forEach(element => {
    element.textContent = `Creation date: ${dateString}`;
  });
}