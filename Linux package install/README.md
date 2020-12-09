## Ansible playbook to install a linux package by taking the package name as an argument

- These playbooks should be under the following directory:
```
/etc/ansible/playbooks
```

- Run the playbook to install a linux package by passing its name as an argument "apache2 in this example" by using the following command:
```
ansible-playbook linux_package.yml --extra-vars "pkg=apache2"
```
