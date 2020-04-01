.requirements.txt: Pipfile Pipfile.lock
	pipenv lock -r > .requirements.txt

.requirements: .requirements.txt
	rm -rf .requirements
	mkdir .requirements
	pip install -r .requirements.txt --no-deps -t .requirements

package.zip: .requirements *.py
	rm -rf package.zip
	(cd .requirements ; zip ../package.zip -r *)
	cd ..
	zip package.zip *.py

.PHONY: deploy
deploy: package.zip
	aws lambda update-function-code --region eu-west-2 --function-name fetch_by_postcode --zip-file fileb://package.zip --publish
