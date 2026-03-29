(() => {
	async function initializeCategoryTabs() {
		const tabsContainer = document.querySelector('.js-category-tabs');
		if (!tabsContainer) {
			return;
		}

		if (tabsContainer.dataset.bound === '1') {
			return;
		}
		tabsContainer.dataset.bound = '1';

		const regionId = tabsContainer.dataset.regionId;
		const targetContainerId = tabsContainer.dataset.targetContainer || 'category-scope-container';
		const loaderTemplate = document.querySelector('.js-category-loader-template');
		const loaderHtml = loaderTemplate ? loaderTemplate.innerHTML : '<div style="padding:8px 0;">Загрузка...</div>';

		async function loadCategoryInfo(categoryId, regionIdArg, targetId) {
			const target = document.getElementById(targetId);
			if (!target || !categoryId || !regionIdArg) {
				return;
			}

			target.innerHTML = loaderHtml;
			const requestUrl = `/indicators/category/${categoryId}?region_id=${regionIdArg}`;

			try {
				const response = await fetch(requestUrl);

				if (!response.ok) {
					target.innerHTML = '<div style="padding:8px 0; color:#b00020;">Ошибка загрузки данных</div>';
					return;
				}

				const html = await response.text();
				target.innerHTML = html;
			} catch {
				target.innerHTML = '<div style="padding:8px 0; color:#b00020;">Ошибка загрузки данных</div>';
			}
		}

		tabsContainer.addEventListener('click', (event) => {
			const tab = event.target.closest('.js-category-tab');
			if (!tab || !tabsContainer.contains(tab)) {
				return;
			}

			tabsContainer.querySelectorAll('.js-category-tab').forEach((item) => item.classList.remove('active'));
			tab.classList.add('active');

			loadCategoryInfo(tab.dataset.categoryId, regionId, targetContainerId);
		});

		const firstTab = tabsContainer.querySelector('.js-category-tab');
		if (firstTab) {
			firstTab.classList.add('active');
			await loadCategoryInfo(firstTab.dataset.categoryId, regionId, targetContainerId);
		}
	}

	if (document.readyState === 'loading') {
		document.addEventListener('DOMContentLoaded', initializeCategoryTabs, { once: true });
	} else {
		initializeCategoryTabs();
	}
})();
