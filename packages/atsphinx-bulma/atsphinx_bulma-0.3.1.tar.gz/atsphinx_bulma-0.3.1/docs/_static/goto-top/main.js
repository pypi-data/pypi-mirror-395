document.addEventListener("DOMContentLoaded", () => {
	// Bind button from template
	const template = document.getElementById("tmpl_gotoTop");
	const elm = template.content.cloneNode(true);
	elm.querySelector("button").addEventListener("click", () => {
		window.scrollTo({ top: 0, behavior: "smooth" });
	});
	document.body.appendChild(elm);

	// Ref element and hook
	const button = document.getElementById("gotoTop");
	const footer = document.querySelector("footer");
	const update = () => {
		const scrolled = window.scrollY;
		const windowHeight = window.innerHeight;
		const documentHeight = document.documentElement.scrollHeight;
		const footerRect = footer.getBoundingClientRect();
		const footerVisible =
			footerRect.top < windowHeight && footerRect.bottom > 0;
		button.style.display =
			documentHeight <= windowHeight || scrolled === 0 ? "none" : "block";
		button.style.bottom = `calc(${footerVisible ? windowHeight - footerRect.top : 0}px + 1rem)`;
	};

	// Bind and call-once hook
	window.addEventListener("scroll", update);
	window.addEventListener("resize", update);
	update();
});
