    const themeDark = () => {
      document.querySelector("body").setAttribute("data-bs-theme", "dark");
      document
        .querySelector("#dl-icon")
        .setAttribute("class", "bi bi-sun-fill");
    };
    const themeLight = () => {
      document.querySelector("body").setAttribute("data-bs-theme", "light");
      document
        .querySelector("#dl-icon")
        .setAttribute("class", "bi bi-moon-fill");
    };
    const changeTheme = () => {
      document.querySelector("body").getAttribute("data-bs-theme") === "light"
        ? themeDark()
        : themeLight();
    };

    function showNext(nextId) {
      const nextElement = document.getElementById(nextId);
      if (nextElement) {
        nextElement.style.display = "block";
      }
    }

    function handleMaterialSelection() {
      const material = document.getElementById("material").value;
      console.log(material)
      const acidGasLoadingGroup = document.getElementById(
        "acidGasLoading-group"
      );
      const acidGasLoadingInfo = document.getElementById(
        "acidGasLoading-info"
      );
      const temperatureGroup = document.getElementById("temperature-group");
      const typeAmineGroup = document.getElementById("typeAmine-group");
      const amineConcentrationGroup = document.getElementById(
        "amineConcentration-group"
      );
      const HSAScontentGroup = document.getElementById("HSAScontent-group");
      const velocityGroup = document.getElementById("velocity-group");
      const buttonGroup = document.getElementById("button-group");
      // const fileUploadGroup = document.getElementById("fileUpload-group");

      if (material === "CS" || material === "Low Alloy Steel") {
        console.log('CS', material)
        temperatureGroup.style.display = "block";
        acidGasLoadingGroup.setAttribute('oninput', 'showNext(\'typeAmine-group\')');
        // fileUploadGroup.style.display = "none";
        acidGasLoadingGroup.style.display = "none";
        acidGasLoadingInfo.style.display = 'none';
        typeAmineGroup.style.display = "none";
        buttonGroup.style.display = "none";
      } else if (material === "300 Series SS") {
        console.log('300')
        temperatureGroup.style.display = "none";
        // fileUploadGroup.style.display = "block";
        acidGasLoadingGroup.style.display = "block";
        acidGasLoadingInfo.style.display = 'block';
        typeAmineGroup.style.display = "none";
        buttonGroup.style.display = "none";
        document.getElementById("acidGasLoading").placeholder = "0.1, 0.15, 0.25, 0.35, 0.45, 0.55, 0.65, 0.7";
      }


    }

    function validateAmineConcentration() {
      const typeAmine = document.getElementById("typeAmine").value;
      const amineConcentrationInput =
        document.getElementById("amineConcentration");
      const amineConcentration = parseFloat(amineConcentrationInput.value);

      let isValid = false;

      if (typeAmine === "MEA") {
        isValid =
          amineConcentration <= 20 ||
          (amineConcentration >= 21 && amineConcentration <= 25) ||
          amineConcentration > 25;
      } else if (typeAmine === "DEA") {
        isValid =
          amineConcentration <= 30 ||
          (amineConcentration >= 31 && amineConcentration <= 40) ||
          amineConcentration > 40;
      } else if (typeAmine === "MDEA") {
        isValid = amineConcentration <= 50;
      }

      if (isValid) {
        amineConcentrationInput.setCustomValidity("");
        showNext("HSAScontent-group");
      } else {
        amineConcentrationInput.setCustomValidity(
          "Invalid concentration for the selected amine type."
        );
        amineConcentrationInput.reportValidity();
      }
    }

    function updatePlaceholder() {
      const typeAmine = document.getElementById("typeAmine").value;
      const amineConcentrationInput =
        document.getElementById("amineConcentration");

      if (typeAmine === "MEA") {
        amineConcentrationInput.placeholder =
          "Allowed Values: ≤20, 21-25, >25";
      } else if (typeAmine === "DEA") {
        amineConcentrationInput.placeholder =
          "Allowed Values: ≤30, 31-40, >40";
      } else if (typeAmine === "MDEA") {
        amineConcentrationInput.placeholder = "Allowed Values: ≤50";
      } else {
        amineConcentrationInput.placeholder = "";
      }
    }

    function calcularCR_300ss() {
      const acidGasLoading = document.getElementById("acidGasLoading").value;

      fetch("/calculate_cr_300ss", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ acidGasLoading: acidGasLoading }),
      })
        .then((response) => response.json())
        .then((data) => {
          const resultDiv = document.getElementById("result");

          // Crear una tabla HTML
          const table = document.createElement("table");
          table.style.width = "100%";
          table.setAttribute("border", "1", "50px");

          // Crear la cabecera de la tabla
          const thead = document.createElement("thead");
          const headerRow = document.createElement("tr");
          const headers = [
            "Acid Gas Loading (mol/mol)",
            "CR (mm/y)",
            "CR (mpy)",
          ];
          headers.forEach((headerText) => {
            const th = document.createElement("th");
            th.appendChild(document.createTextNode(headerText));
            headerRow.appendChild(th);
          });
          thead.appendChild(headerRow);
          table.appendChild(thead);

          // Crear el cuerpo de la tabla
          const tbody = document.createElement("tbody");
          const row = document.createElement("tr");

          const values = [
            acidGasLoading,
            data.cr_mm_year.toFixed(2),
            data.cr_mpy,
          ];
          values.forEach((value) => {
            const td = document.createElement("td");
            td.appendChild(document.createTextNode(value));
            row.appendChild(td);
          });

          tbody.appendChild(row);
          table.appendChild(tbody);

          // Limpiar el contenido previo y añadir la nueva tabla
          resultDiv.innerHTML = "";
          resultDiv.appendChild(table);
        })
        .catch((error) => console.error("Error:", error));
    }

    async function calcularCR() {
      const material = document.getElementById("material").value;
      const temperatureLoading = document.getElementById("temperatureLoading").value;
      const acidGasLoading = document.getElementById("acidGasLoading").value;
      const typeAmine = document.getElementById("typeAmine").value;
      const amineConcentration = document.getElementById("amineConcentration").value;
      const HSAScontent = document.getElementById("HSAScontent").value;
      const velocity = document.getElementById("velocity").value;

      // Preparar los datos para enviar
      const requestData = {
        acid_gas_loading: parseFloat(acidGasLoading),
        temperature: parseInt(temperatureLoading),
        velocity: parseFloat(velocity),
        hsas: parseFloat(HSAScontent)
      };

      try {
        // Realizar la solicitud POST a la API
        const response = await fetch('/api/buscar_cr', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify(requestData)
        });

        // Procesar la respuesta
        if (response.ok) {
          const result = await response.json();
          const cr = result.cr;

          // Crear la tabla con los resultados
          const table = document.createElement("table");
          table.style.width = "100%";
          table.setAttribute("border", "1");

          // Crear la cabecera de la tabla
          const thead = document.createElement("thead");
          const headerRow = document.createElement("tr");
          const headers = [
            "Material",
            "Operating Temperature",
            "Acid Gas Load",
            "Amine Type",
            "Amine Concentration",
            "HSAS",
            "Velocity"
          ];
          headers.forEach((headerText) => {
            const th = document.createElement("th");
            th.appendChild(document.createTextNode(headerText));
            headerRow.appendChild(th);
          });
          thead.appendChild(headerRow);
          table.appendChild(thead);

          // Crear el cuerpo de la tabla
          const tbody = document.createElement("tbody");
          const row = document.createElement("tr");

          const values = [
            material,
            temperatureLoading,
            acidGasLoading,
            typeAmine,
            amineConcentration,
            HSAScontent,
            velocity
          ];
          values.forEach((value) => {
            const td = document.createElement("td");
            td.appendChild(document.createTextNode(value));
            row.appendChild(td);
          });

          tbody.appendChild(row);
          table.appendChild(tbody);

          // Limpiar el contenido previo y añadir la nueva tabla
          const resultDiv = document.getElementById("result");
          resultDiv.innerHTML = "";
          resultDiv.appendChild(table);
        } else {
          const errorData = await response.json();
          document.getElementById("result").innerHTML = `<p>${errorData.error}</p>`;
        }
      } catch (error) {
        document.getElementById("result").innerHTML = `<p>Error al realizar la solicitud: ${error.message}</p>`;
      }
    }

