import 'package:client/core/theme/app_palette.dart';
import 'package:client/features/auth/view/widgets/auth_gradient_button.dart';
import 'package:client/features/auth/view/widgets/custom_field.dart';
import 'package:flutter/material.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();
  final formKey = GlobalKey<FormState>();

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
    formKey.currentState!.validate();
  }
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(),
      body: Padding(
        padding: const EdgeInsets.all(15.0),
        child: Form(
          key: formKey,
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Text(
                'Sign In.', 
                style: TextStyle(
                fontSize: 50,
                fontWeight: FontWeight.bold,
          
              ),
              ),
              const SizedBox(height: 30,),
              CustomField(
                hintText: 'Email',
                controller: emailController,
              ),
              const SizedBox(height: 15),
               CustomField(
                hintText: 'Password',
                controller: passwordController,
                isObscureText: true,
              ),
              const SizedBox(height: 20),
              AuthGradientButton(
                buttonText: "Sign in",
                onTap:() async {
                  await AuthRemoteRepository().login(
                    email: emailController.text,
                    password: passwordController.text,
                  );

                  final val = switch(res) {
                    Left(value: final l) => l,
                    Right(value: final r) => r,
                  };
                  print(va);
                },
              ),
              const SizedBox(height: 20),
              GestureDetector(
                   onTap: () {
                        Navigator.push(
                          context,
                          MaterialPageRoute(
                            builder: (context) => const LoginPage(),
                          ),
                        );
                   },
                child: RichText(
                text:TextSpan(
                text: 'Dont have an account? ',
                style: Theme.of(context).textTheme.titleMedium,
                children: const [
                  TextSpan(
                    text: 'Sign Up',
                    style: TextStyle(
                      color: Palette.gradient2,
                      fontWeight: FontWeight.bold,
                    ),
                  
                  ),
                ],
              ) ,
              ),
              ),
            ],
          ),
        ),
      ),

    );
  }
}