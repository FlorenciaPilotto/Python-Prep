import 'package:flutter/material.dart';

void main() {
  runApp(const EjeApp());
}

class EjeApp extends StatelessWidget {
  const EjeApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'EJE',
      theme: ThemeData(
        brightness: Brightness.dark,
        scaffoldBackgroundColor: const Color(0xFF0B0B0D),
        colorScheme: const ColorScheme.dark(
          primary: Color(0xFF8FAF9A),
          surface: Color(0xFF0B0B0D),
        ),
        textTheme: const TextTheme(
          headlineMedium: TextStyle(color: Color(0xFFF1F1F1), fontWeight: FontWeight.w600),
          bodyLarge: TextStyle(color: Color(0xFFF1F1F1)),
          bodyMedium: TextStyle(color: Color(0xFFB7B7B7)),
        ),
      ),
      home: const LandingScreen(),
    );
  }
}

class OnboardingData {
  String email = '';
  String estadoMental = '';
  String cardToken = '';
}

class AppScaffold extends StatelessWidget {
  final String title;
  final Widget child;
  final Widget? footer;

  const AppScaffold({
    super.key,
    required this.title,
    required this.child,
    this.footer,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 24, vertical: 20),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Text(title, style: Theme.of(context).textTheme.headlineMedium),
              const SizedBox(height: 28),
              Expanded(child: child),
              if (footer != null) ...[
                const SizedBox(height: 16),
                footer!,
              ],
            ],
          ),
        ),
      ),
    );
  }
}

class LandingScreen extends StatelessWidget {
  const LandingScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'EJE',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text('Precisión, silencio, control.', style: Theme.of(context).textTheme.bodyMedium),
          const Spacer(),
          FilledButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => RegisterScreen(data: OnboardingData())),
              );
            },
            child: const Text('Comenzar prueba gratuita'),
          ),
          const SizedBox(height: 8),
          const Text('7 días gratis. Luego USD 7/mes.', textAlign: TextAlign.center),
        ],
      ),
    );
  }
}

class RegisterScreen extends StatefulWidget {
  final OnboardingData data;
  const RegisterScreen({super.key, required this.data});

  @override
  State<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends State<RegisterScreen> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Creá tu acceso.',
      child: Column(
        children: [
          TextField(
            controller: _emailController,
            decoration: const InputDecoration(labelText: 'Email'),
          ),
          const SizedBox(height: 16),
          TextField(
            controller: _passwordController,
            obscureText: true,
            decoration: const InputDecoration(labelText: 'Contraseña'),
          ),
          const SizedBox(height: 16),
          const Text('No enviamos spam. Solo acceso a tu entrenamiento.'),
          const Spacer(),
          FilledButton(
            onPressed: () {
              widget.data.email = _emailController.text.trim();
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => EmotionalScreen(data: widget.data)),
              );
            },
            child: const Text('Continuar'),
          ),
        ],
      ),
    );
  }
}

class EmotionalScreen extends StatefulWidget {
  final OnboardingData data;
  const EmotionalScreen({super.key, required this.data});

  @override
  State<EmotionalScreen> createState() => _EmotionalScreenState();
}

class _EmotionalScreenState extends State<EmotionalScreen> {
  static const options = ['Saturada', 'Ansiosa', 'Dispersa', 'Cansada', 'Clara pero tensa'];
  String? selected;

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: '¿Cómo está tu mente hoy?',
      child: Column(
        children: [
          ...options.map(
            (option) => Padding(
              padding: const EdgeInsets.only(bottom: 10),
              child: OutlinedButton(
                onPressed: () => setState(() => selected = option),
                style: OutlinedButton.styleFrom(
                  side: BorderSide(
                    color: selected == option ? const Color(0xFF8FAF9A) : const Color(0xFF4A4A4A),
                  ),
                ),
                child: Align(alignment: Alignment.centerLeft, child: Text(option)),
              ),
            ),
          ),
          const Spacer(),
          FilledButton(
            onPressed: selected == null
                ? null
                : () {
                    widget.data.estadoMental = selected!;
                    Navigator.push(
                      context,
                      MaterialPageRoute(builder: (_) => PaymentScreen(data: widget.data)),
                    );
                  },
            child: const Text('Continuar'),
          ),
        ],
      ),
    );
  }
}

class PaymentScreen extends StatefulWidget {
  final OnboardingData data;
  const PaymentScreen({super.key, required this.data});

  @override
  State<PaymentScreen> createState() => _PaymentScreenState();
}

class _PaymentScreenState extends State<PaymentScreen> {
  final _cardController = TextEditingController();

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Activá tu prueba gratuita.',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('7 días gratis.\nLuego USD 7/mes.\nCancelás cuando quieras.'),
          const SizedBox(height: 20),
          TextField(
            controller: _cardController,
            decoration: const InputDecoration(labelText: 'Tarjeta'),
          ),
          const SizedBox(height: 10),
          const Text('Te avisamos antes de que termine tu prueba.'),
          const Spacer(),
          FilledButton(
            onPressed: () {
              widget.data.cardToken = _cardController.text.trim();
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => ConfirmationScreen(data: widget.data)),
              );
            },
            child: const Text('Comenzar entrenamiento'),
          ),
        ],
      ),
    );
  }
}

class ConfirmationScreen extends StatelessWidget {
  final OnboardingData data;
  const ConfirmationScreen({super.key, required this.data});

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Bienvenida a EJE.',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Tu mente ya empezó a bajar la interferencia.'),
          const Spacer(),
          FilledButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (_) => FirstSessionScreen(data: data)),
              );
            },
            child: const Text('Comenzar primera sesión'),
          ),
        ],
      ),
    );
  }
}

class FirstSessionScreen extends StatefulWidget {
  final OnboardingData data;
  const FirstSessionScreen({super.key, required this.data});

  @override
  State<FirstSessionScreen> createState() => _FirstSessionScreenState();
}

class _FirstSessionScreenState extends State<FirstSessionScreen> {
  bool started = false;

  @override
  Widget build(BuildContext context) {
    return AppScaffold(
      title: 'Reset Inicial',
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text('Reducir interferencia básica.'),
          const SizedBox(height: 8),
          Text('Estado detectado: ${widget.data.estadoMental}'),
          const SizedBox(height: 8),
          const Text('Voz: femenina'),
          const Text('Audio enfoque: https://www.youtube.com/watch?v=ilXtdnLsZVg'),
          const Spacer(),
          FilledButton(
            onPressed: () => setState(() => started = true),
            child: Text(started ? 'Sesión en curso...' : 'Iniciar'),
          ),
          if (started) ...[
            const SizedBox(height: 12),
            const Text('✔ Primera sesión iniciada (3 min).'),
          ],
        ],
      ),
    );
  }
}
