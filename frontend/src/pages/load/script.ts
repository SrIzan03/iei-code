export const cle = "cle"
export const cv = "cv"
export const eus = "eus"
export const allSelected = "all-selected"
export const loadResult = "load-result"
const url = 'http://localhost:8080';

function getCheckboxContainer() {
    return document.getElementById("checkbox-container");
}

function getCheckedValues() {
    const container = getCheckboxContainer()
    if (container == null) {
        return;
    }

    const checkBoxes = Array.from(container.querySelectorAll<HTMLInputElement>("input[type='checkbox']"))

    return checkBoxes
        .filter(c => c.checked)
        .map(c => c.id)
}

function setLoading() {
    const resultContainer = document.getElementById(loadResult)
        if (resultContainer == null) {
            return;
        }

    resultContainer.textContent = "Cargando..."
}

async function loadMonuments() {
    setLoading()

    const loadUrl = url + "/data";

    const loadEus = loadUrl + "/" + eus
    const loadCv = loadUrl + "/" + cv
    const loadCle = loadUrl + "/" + cle

    const logUrl = url + "/logs"

    const loaders = new Map<string, string>()
    loaders.set(eus, loadEus)
    loaders.set(cv, loadCv)
    loaders.set(cle, loadCle)

    let checkedValues = getCheckedValues()
    if (checkedValues == null) {
        return;
    }

    if (checkedValues.includes(allSelected)) {
        checkedValues = [eus, cv, cle]
    }

    for (const value of checkedValues) {
        const loader = loaders.get(value)
        if (loader == null) {
            return;
        }

        const response = await fetch(loader, {
            method: 'POST'
        });
        if (response.ok) {
            console.log(response.json())
        }

    }

    const response = await fetch(logUrl)
    if (response.ok) {
        const resultContainer = document.getElementById(loadResult)
        if (resultContainer == null) {
            return;
        }
        const content = await response.json()
        resultContainer.textContent = content
    }
}

async function deleteMonuments() {
    setLoading()
    
    const deleteResponse = await fetch(url + "/database/reset", {
        method: 'POST'
    });
    if (deleteResponse.ok) {
        const resultContainer = document.getElementById(loadResult)
        if (resultContainer == null) {
            return;
        }

        resultContainer.textContent = "Eliminado correctamente"
    }
}

function addLoadButtonAction() {
    const loadButton = document.getElementById("load-btn");
    if (loadButton == null) {
        return;
    }

    loadButton.onclick = loadMonuments
}

function addDeleteButtonAction() {
    const deleteButton = document.getElementById("delete-btn")
    if (deleteButton == null) {
        return;
    }

    deleteButton.onclick = deleteMonuments
}

export function addButtonsActions() {
    addLoadButtonAction()
    addDeleteButtonAction()
}

export function addCheckboxEventListeners() {
    const container = getCheckboxContainer()

    if (container == null) {
        return;
    }

    const allSelected = document.getElementById("all-selected") as HTMLInputElement;
    const others = Array.from(container.querySelectorAll<HTMLInputElement>("input[type='checkbox']:not(#all-selected)"));

    if (allSelected == null || others == null) {
        return;
    }

    allSelected.addEventListener("change", (event) => {
        if (event == null || event.target == null) {
            return;
        }
        const target = event.target as HTMLInputElement;

        if (target.checked) {
            others.forEach((checkbox) => (checkbox.checked = false));
        }
    });

    others.forEach((checkbox) => {
        checkbox.addEventListener("change", () => {
            if (checkbox.checked) {
                allSelected.checked = false;
            }
        });
    });
}