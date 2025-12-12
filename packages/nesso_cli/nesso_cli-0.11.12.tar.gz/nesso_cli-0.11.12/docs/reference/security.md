# Security

In the last few years, with the rise of large scale cybercrime such as state-sponsored groups or ransomware gangs, security is becoming a bigger and bigger concern for all organizations.

There are many techniques and tools to increase security. However, the two main principles are quite simple:

- keeping the infrastructure as simple as possible  
- enforcing security best practices from users, hopefully by encoding them into workflows and tools  

We can add one more, although this one is only useful in case a security breach has already ocurred:

- [principle of least privilege](https://en.wikipedia.org/wiki/Principle_of_least_privilege) 

We believe that the Git workflow is the best way to ensure security of the data product development process. It allows us to utilize the following security best practices:

- simplicity  
Simplicity is one of the most powerful ways to ensure security. The more complex the system, the more likely it is to have security vulnerabilities. And, as all  software engineers are well aware, in IT, complexity grows exponentially. Removing just a few parts often has a dramatic impact on the complexity of a system.  In fact, sometimes even adding a new security component can increase the complexity enough that it makes the overall system more vulnerable. **Beware of any person, product, or company adding esoteric security features without thoroughly considering their impact on the complexity of the system and user workflows.**

    Re-using existing tooling such as Git simplifies the system and reduces the number of moving parts.

- security best practices  
This is likely the most overlooked, but also by far the most important principle. As a reminder, **vast majority of cyber attacks result from gaining unauthorized access to employee account(s)**, typically through the use of phishing.

    There are numerous techniques to ensure user accounts are protected. Some of the biggest security weaknesses in this area are:

    - storing passwords in multiple places (solved by password managers)
    - providing the same password in multiple places (solved by SSO and social logins)
    - using passwords in the first place (solved by a few techniques, eg. passkeys, SSH keys, security keys)
    - not using multi-factor authentication (MFA)
    - principle of least privilege
        - the analyst does not have direct write access to production schemas
        - the analysts does not have direct write access to the data catalog

Git providers, such as GitHub, provide best security practices that solve all above problems:

- **SSH keys** for authentication when accessing Git through the CLI
- **passkey** and **MFA** for authentication when accessing Git through the browser
- **Pull Request** process to ensure that no one can directly edit production data or metadata
