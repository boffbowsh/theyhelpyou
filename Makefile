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

.PHONY: deploy s3
deploy: package.zip
	aws lambda update-function-code --region eu-west-2 --function-name fetch_by_postcode --zip-file fileb://package.zip --publish

s3: site/index.html
	aws s3 cp site/index.html s3://theyhelpyou/index.html --acl public-read
