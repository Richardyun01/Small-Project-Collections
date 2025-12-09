document.addEventListener("DOMContentLoaded", function () {
    const domainInput = document.getElementById("domainInput");
    const addDomainBtn = document.getElementById("addDomain");
    const domainList = document.getElementById("domainList");

    // 저장된 도메인 목록 불러오기
    chrome.storage.sync.get({ blockedDomains: [] }, function (data) {
        data.blockedDomains.forEach(domain => addDomainToList(domain));
    });

    // 도메인 추가 버튼 클릭 이벤트
    addDomainBtn.addEventListener("click", function () {
        const domain = domainInput.value.trim();
        if (domain === "") return;

        // 저장된 목록 가져와서 업데이트
        chrome.storage.sync.get({ blockedDomains: [] }, function (data) {
            let domains = data.blockedDomains;

            if (!domains.includes(domain)) {
                domains.push(domain);
                chrome.storage.sync.set({ blockedDomains: domains }, function () {
                    addDomainToList(domain);
                    domainInput.value = ""; // 입력 필드 초기화
                });
            }
        });
    });

    // 리스트에 도메인 추가하는 함수
    function addDomainToList(domain) {
        const li = document.createElement("li");
        li.textContent = domain;

        const deleteBtn = document.createElement("button");
        deleteBtn.textContent = "X";
        deleteBtn.style.marginLeft = "10px";
        deleteBtn.style.cursor = "pointer";

        deleteBtn.addEventListener("click", function () {
            removeDomain(domain, li);
        });

        li.appendChild(deleteBtn);
        domainList.appendChild(li);
    }

    // 도메인 삭제하는 함수
    function removeDomain(domain, listItem) {
        chrome.storage.sync.get({ blockedDomains: [] }, function (data) {
            let domains = data.blockedDomains.filter(d => d !== domain);
            chrome.storage.sync.set({ blockedDomains: domains }, function () {
                listItem.remove();
            });
        });
    }
});
