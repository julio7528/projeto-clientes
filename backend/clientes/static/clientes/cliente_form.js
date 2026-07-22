(() => {
  const form = document.querySelector("[data-cliente-form]");
  if (!form) return;

  const type = form.querySelector("[name='tipo']");
  const documentInput = form.querySelector("[name='documento']");
  const phone = form.querySelector("[name='telefone']");
  const cep = form.querySelector("[name='cep']");
  const nameLabel = form.querySelector("label[for='id_nome']");
  const documentLabel = form.querySelector("label[for='id_documento']");
  const dateLabel = form.querySelector("label[for='id_data_referencia']");
  let previousType = form.dataset.initialType || "PF";

  const digits = (value) => value.replace(/\D/g, "");
  const maskDocument = () => {
    const value = digits(documentInput.value).slice(0, type.value === "PJ" ? 14 : 11);
    documentInput.value = type.value === "PJ"
      ? value.replace(/^(\d{2})(\d)/, "$1.$2").replace(/^(\d{2})\.(\d{3})(\d)/, "$1.$2.$3").replace(/\.(\d{3})(\d)/, ".$1/$2").replace(/(\d{4})(\d)/, "$1-$2")
      : value.replace(/^(\d{3})(\d)/, "$1.$2").replace(/\.(\d{3})(\d)/, ".$1.$2").replace(/(\d{3})(\d)/, "$1-$2");
  };
  const maskPhone = () => {
    const value = digits(phone.value).slice(0, 11);
    phone.value = value.replace(/^(\d{2})(\d)/, "($1) $2").replace(/(\d{4,5})(\d{4})$/, "$1-$2");
  };
  const maskCep = () => {
    cep.value = digits(cep.value).slice(0, 8).replace(/(\d{5})(\d)/, "$1-$2");
  };
  const updateLabels = () => {
    const isPJ = type.value === "PJ";
    nameLabel.textContent = isPJ ? "Nome empresarial" : "Nome completo";
    documentLabel.textContent = isPJ ? "CNPJ" : "CPF";
    dateLabel.textContent = isPJ ? "Data de abertura" : "Data de nascimento";
  };

  type.addEventListener("change", () => {
    if (documentInput.value && !window.confirm("Ao alterar o tipo de cliente, o documento informado será removido. Continuar?")) {
      type.value = previousType;
      return;
    }
    previousType = type.value;
    documentInput.value = "";
    updateLabels();
  });
  documentInput.addEventListener("input", maskDocument);
  phone.addEventListener("input", maskPhone);
  cep.addEventListener("input", maskCep);
  form.addEventListener("submit", () => {
    documentInput.value = digits(documentInput.value);
    phone.value = digits(phone.value);
    cep.value = digits(cep.value);
    form.querySelectorAll("button[type='submit']").forEach((button) => { button.disabled = true; });
  });
  updateLabels();
})();
